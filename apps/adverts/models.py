from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.signals import pre_save
from mptt.models import MPTTModel, TreeForeignKey, raise_if_unsaved
from json import JSONEncoder

# from adverts.helpers.json_parse import StringParse


class Region(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_full_slug(self):
        slugs = self.get_ancestors(include_self=True).values('slug')
        full_slug = '/'.join(map(lambda x: x['slug'], slugs))
        return full_slug

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
    # cat = GenericForeignKey('content_type', 'category_id')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=Kinds.choices)
    # required = models.BooleanField()
    variants = ArrayField(
        models.CharField(max_length=255),
        size=10
    )
    sort = models.IntegerField()

    def is_select(self):
        return len(self.variants) > 1





