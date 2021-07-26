from cities_light.models import City as BaseCity
from transliterate import translit, get_available_language_codes
from django.contrib.auth.models import User
from django.utils.text import slugify

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
# from django.db.models.query import Prefetch
from django.db.models import Prefetch
from django.db.models.signals import pre_save, post_save
from django.shortcuts import redirect
from mptt.models import MPTTModel, TreeForeignKey, raise_if_unsaved
from json import JSONEncoder


# class City(BaseCity):
#
#     def get_display_name(self):
#         if self.region_id:
#             return '%s, %s, %s' % (self.alternate_names, self.region.alternate_names,
#                                    self.country.alternate_names)
#         else:
#             return '%s, %s' % (self.alternate_names, self.country.alternate_names)
#
    # class Meta:
        # db_table = 'cities_light_city'


class Location(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=False, max_length=255, default=None, null=True, blank=True)
    address = models.CharField(max_length=255, unique=False, default=None, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_full_name(self):
        names = self.get_ancestors(include_self=True).values('name')
        full_name = '/'.join(map(lambda x: x['name'], names))
        return full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.name and not self.slug:
            self.slug = slugify(translit(self.get_full_name().replace('/', '-'), 'uk', reversed=True))
        if self.name and not self.address:
            self.address = self.get_full_name()
        super().save(*args, **kwargs)

    # def get_child(self):
    #     return self.children.select_related('parent').filter(level__in=[self.level + 1])

    class Meta:
        ordering = ['lft']

    class MPTTMeta:
        order_insertion_by = ['name']


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_full_slug(self):
        slugs = self.get_ancestors(include_self=True).values('slug')
        full_slug = '/'.join(map(lambda x: x['slug'], slugs))
        return full_slug

    def all_attributes(self):
        return self.parent_attributes() + list(self.attribute_set.all())

    def parent_attributes(self):
        return self.parent.all_attributes() if self.parent else []

    def get_name(self):
        return self.name

    class Meta:
        ordering = ['lft']

    class MPTTMeta:
        order_insertion_by = ['name']


class Attribute(models.Model):

    class Kinds(models.TextChoices):
        TYPE_STRING = 'string', 'String'
        TYPE_INTEGER = 'integer', 'Integer'
        TYPE_FLOAT = 'float', 'Float'
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attribute_set')
    category = TreeForeignKey(Category, on_delete=models.CASCADE, related_name='attribute_set')
    name = models.CharField(max_length=200, validators=[])
    type = models.CharField(max_length=50, choices=Kinds.choices)
    required = models.BooleanField(default=False)
    variants = ArrayField(
        models.CharField(max_length=255, default='', blank=True, null=True),
        size=10,
        blank=True
    )
    sort = models.IntegerField()

    def __str__(self):
        return self.name

    def is_select(self):
        return len(self.variants) > 0

    # its work but not effect

    # def is_available_attribute_name(self):
    #     family = self.category.get_family()
    #     for category in family:
    #         attributes = category.all_attributes()
    #         print(attributes)
    #         for attr in attributes:
    #             if self.name == attr.name:
    #                 return False
    #     return True

    # worked version 13 queries

    # def is_available_attribute_name(self):
    #     family = self.category.get_family()
    #     ids = [obj.id for obj in family]
    #     categories = self.category.get_family().prefetch_related('attribute_set').all()
    #     for category in categories:
    #         # print(attribute)
    #         for attr in category.attribute_set.prefetch_related('category').filter(category_id__in=ids):
    #             if attr.name == self.name:
    #                 return False
    #     return True

    # def is_available_attribute_name(self):
    #     categories = self.category.get_family()
    #     ids = [obj.id for obj in categories]
    #     for category in categories:
    #         # print(attribute)
    #         for attr in category.attribute_set.prefetch_related(Prefetch('category', queryset=Category.objects.filter(id__in=ids))):
    #             if attr.name == self.name:
    #                 return False
    #     return True

    def is_available_attribute_name(self):
        categories = self.category.get_family()
        ids = [obj.id for obj in categories]
        for category in categories:
            attributes = category.attribute_set.filter(category_id__in=ids)
            for attr in attributes:
                if attr.name == self.name and not self.pk:
                    return False
        return True

    def clean(self):
        if not self.is_available_attribute_name():
            raise ValidationError(f'attribute name "{self.name}" already exist in parent category')

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):



        # family = self.category.get_family()
        # for category in family:
        #     attributes = category.objects.prefetch_related('attribute_set').value_list('attribute_set__name', flat=True)
        #     for attr in attributes:
        #
        #
        #         if self.name == attr:
        #             print('!')
        # super().save(force_insert=False, force_update=False, using=None,
        #      update_fields=None)

    class Meta:
        unique_together = ('category', 'name')


class AdvertsAdvert(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_MODERATION = 'moderation'
    STATUS_ACTIVE = 'active'
    STATUS_CLOSED = 'closed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_set')
    category = TreeForeignKey(Category, on_delete=models.PROTECT, related_name='category_set')
    location = TreeForeignKey(Location, on_delete=models.PROTECT, related_name='location_set')
    # location = models.ForeignKey(City, on_delete=models.PROTECT, related_name='location_set')
    title = models.CharField(max_length=255)
    price = models.FloatField()
    currency = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default=STATUS_DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # value = models.ManyToManyField('Value', related_name='value_set')

    def get_value(self, attribute_id):
        for value in self.advert_to_attribute.all():
            if value.attribute.id == attribute_id:
                return value.value
        return

    def get_all_values(self):
        return self.advert_to_attribute.all()

    def get_category(self):
        return self.category


class Value(models.Model):
    advert = models.ForeignKey(AdvertsAdvert, on_delete=models.PROTECT, related_name='advert_to_attribute')
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='attribute_to_advert')
    value = models.CharField(max_length=255)

    def get_attribute_id(self):
        return self.attribute_id

    def get_attribute(self):
        return self.attribute.name

    def get_value(self):
        return self.value

    class Meta:
        unique_together = ('advert', 'attribute')
