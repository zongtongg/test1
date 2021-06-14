from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
# from django.db.models.query import Prefetch
from django.db.models import Prefetch
from django.db.models.signals import pre_save
from django.shortcuts import redirect
from mptt.models import MPTTModel, TreeForeignKey, raise_if_unsaved
from json import JSONEncoder

# from adverts.helpers.json_parse import StringParse
# from apps.adverts.validators import attribute_name_validator


# class Location(models.Model):
#     test_id = models.IntegerField()
#     region = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#
#     class Meta:
#         db_table = 'location'


class Location(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default=None, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_full_name(self):
        names = self.get_ancestors(include_self=True).values('name')
        full_name = '/'.join(map(lambda x: x['name'], names))
        return full_name

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
    # category_id = models.PositiveIntegerField()
    name = models.CharField(max_length=200, validators=[])
    type = models.CharField(max_length=50, choices=Kinds.choices)
    # required = models.BooleanField()
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
                if attr.name == self.name:
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

