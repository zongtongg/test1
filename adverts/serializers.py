from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from adverts.models import Region, Category, Attribute


class BaseTreeSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=50)
    slug = serializers.SlugField(max_length=50)
    path = serializers.ReadOnlyField(source='get_full_slug')
    children = serializers.ListField(read_only=True, required=False, source='get_children', child=RecursiveField())

    class Meta:
        fields = ('id', 'name', 'slug', 'path', 'children')


class RegionsSerializer(BaseTreeSerializer):

    class Meta:
        model = Region


class AttributeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=50, read_only=True)
    # required = serializers.BooleanField()
    variants = serializers.JSONField(
        serializers.CharField(max_length=255)
    )
    sort = serializers.IntegerField(read_only=True)

    class Meta:
        model = Attribute
        fields = ('id', 'name', 'type', 'variants', 'sort')


class CategoriesSerializer(BaseTreeSerializer):
    attributes = AttributeSerializer(source='attribute_set', many=True)

    class Meta:
        model = Category

        fields = ('id', 'name', 'slug', 'path',  'attributes', 'children')


class SingleCategorySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=50)
    slug = serializers.SlugField(max_length=50)
    attributes = AttributeSerializer(source='attribute_set', many=True)
    all_attr = AttributeSerializer(source='all_attributes', many=True)

    class Meta:
        model = Category
        depth = 1
        fields = ('id', 'name', 'slug', 'attributes', 'all_attr')
