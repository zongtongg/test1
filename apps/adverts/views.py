from django.core.cache import cache
from django.shortcuts import render
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from apps.adverts.models import Location, Category, Attribute
from apps.adverts.serializers import LocationsSerializer, CategoriesSerializer, SingleCategorySerializer


def test(request):
    attributes = Attribute.objects.filter(name='collor')

    return render(request, 'adverts/attribute.html', {'attributes': attributes})


class LocationView(APIView):
    def get(self, request, pk):
        location = Location.objects.get(pk=pk)
        key = request.META.get('PATH_INFO')
        result = get_items_from_cache(key, location, LocationsSerializer)
        return Response({'locations': result})


class CategoryView(APIView):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        key = request.META.get('PATH_INFO')
        result = get_items_from_cache(key, category, CategoriesSerializer)
        return Response({'categories': result})


class SingleCategoryView(APIView):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        key = request.META.get('PATH_INFO')
        result = get_items_from_cache(key, category, SingleCategorySerializer)
        return Response({'categories': result})


def get_items_from_cache(key, item, serializer):
    # get_redis_connection("default").flushall()
    if cache.get(key):
        result = cache.get(key)
    else:
        result = serializer(item).data
        cache.set(key, result, 8)
    return result
