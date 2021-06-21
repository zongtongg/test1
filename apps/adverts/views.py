from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import render
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from apps.adverts.models import Location, Category, Attribute, AdvertsAdvert, Value
from apps.adverts.serializers import LocationsSerializer, CategoriesSerializer, SingleCategorySerializer, \
    AdvertSerializer


def test(request, pk):
    category = Category.objects.get(pk=pk)
    location = Location.objects.all()
    adverts = AdvertsAdvert.objects.all()
    if request.method == 'POST':
        advert = AdvertsAdvert()
        advert.user = request.user
        advert.category = category
        advert.location = Location.objects.get(pk=request.POST.get('location'))
        advert.title = request.POST.get('title')
        advert.price = request.POST.get('price')
        advert.currency = request.POST.get('currency')
        advert.save()
        # for attr in request.POST.get('attr.*'):
        # input_tag = request.POST.find_all(attrs={"name": "attr"})
        # print(input_tag)
        for attribute in category.all_attributes():
            value = request.POST.get('attr.' + str(attribute.id))
            if value:
                val = Value(advert=advert, attribute=attribute, value=value)
                val.save()
                # advert.value.add(val)
                # print(val)
        # print(request.POST)

        return render(request, 'adverts/attribute.html', {'advert': advert})
    return render(request, 'adverts/attribute.html', {'category': category, 'location': location, 'adverts': adverts})


class LocationView(APIView):
    def get(self, request, pk):
        location = Location.objects.select_related('parent').get(pk=pk)
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


class AdvertView(APIView):
    def get(self, request, pk):
        advert = AdvertsAdvert.objects.select_related('category').select_related('location').select_related('user').get(pk=pk)
        # advert.objects.selvect_related('advert_to_attribute')
        data = AdvertSerializer(advert).data
        return Response({'advert': data})


def get_items_from_cache(key, item, serializer):
    # get_redis_connection("default").flushall()
    if cache.get(key):
        result = cache.get(key)
    else:
        result = serializer(item).data
        cache.set(key, result, 8)
    return result
