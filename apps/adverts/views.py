from django.core.cache import cache
from django.shortcuts import render
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from apps.adverts.models import Region, Category, Attribute
from apps.adverts.serializers import RegionsSerializer, CategoriesSerializer, SingleCategorySerializer


def test(request):
    category = Category.objects.get(pk=6)
    return render(request, 'adverts/attribute.html', {'category': category})

class RegionView(APIView):
    def get(self, request, pk):
        region = Region.objects.get(pk=pk)
        key = request.META.get('PATH_INFO')
        result = get_items_from_cache(key, region, RegionsSerializer)
        return Response({'regions': result})


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
