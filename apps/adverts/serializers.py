from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from apps.adverts.models import Location, Category, Attribute, AdvertsAdvert, Value


class BaseTreeSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=50)
    slug = serializers.SlugField(max_length=50)
    # path = serializers.ReadOnlyField(source='get_full_name')
    children = serializers.ListField(read_only=True, required=False, source='get_children', child=RecursiveField())

    class Meta:
        fields = ('id', 'name', 'slug', 'path', 'children')


class LocationsSerializer(BaseTreeSerializer):
    address = serializers.CharField(max_length=255)
    children = serializers.ListField(read_only=True, required=False, source='get_children', child=RecursiveField())

    class Meta:
        model = Location
        fields = ('id', 'name', 'slug', 'path', 'children')


class AttributeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=50, read_only=True)
    # required = serializers.BooleanField()
    variants = serializers.JSONField(
        serializers.CharField(max_length=255)
    )
    sort = serializers.IntegerField(read_only=True)
    is_select = serializers.BooleanField(read_only=True)

    class Meta:
        model = Attribute
        fields = ('id', 'name', 'type', 'variants', 'sort', 'is_select')


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


class ValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='get_attribute_id')
    name = serializers.CharField(max_length=50, source='get_attribute', read_only=True)
    value = serializers.CharField(max_length=50, source='get_value')

    class Meta:
        model = Value
        # fields = ('id', 'name', 'value')
        fields = '__all__'

class AdvertUserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        depth = 2
        fields = ('id', 'username')


class AdvertCategorySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Category
        depth = 2
        fields = ('id', 'name')


class AdvertLocationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Location
        depth = 2
        fields = ('id', 'name')


class AdvertSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = AdvertUserSerializer(many=False)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = AdvertCategorySerializer(many=False)
    location = AdvertLocationSerializer(many=False)
    title = serializers.CharField(max_length=255)
    price = serializers.FloatField()
    currency = serializers.CharField(max_length=50)
    # content = serializers.(blank=True, null=True)
    status = serializers.CharField(max_length=50, default=AdvertsAdvert.STATUS_DRAFT)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    attributes = ValueSerializer(many=True, source='get_all_values', read_only=False)

    class Meta:
        model = AdvertsAdvert
        # depth = 1
        fields = ('id', 'user', 'category', 'location', 'title', 'price', 'currency', 'status', 'created_at',
                  'updated_at', 'attributes')



data = {
"user_id":1,
"category_id":3,
"location_id":3,
"title": "LG",
"price": 100,
"currency": "$",
"attributes": [
    {
        "id": 5,
        "value": "red"
    },
    {
        "id": 5,
        "value": "red"
    }
]
}

