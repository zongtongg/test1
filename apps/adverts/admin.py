from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.adverts.helpers.html_helper import get_mptt_indented_menu
from apps.adverts.models import Location, Category, Attribute, AdvertsAdvert, Value


class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_name')
    list_display_links = ('indented_name',)

    def indented_name(self, instance):
        return get_mptt_indented_menu(self, instance)

    indented_name.short_description = 'something nice'


class LocationMPTTModelAdmin(CustomMPTTModelAdmin):
    list_display_links = ('indented_name',)
    search_fields = ('name',)

    def indented_name(self, instance):
        return super().indented_name(instance)

    indented_name.short_description = 'Location'


class CategoryMPTTModelAdmin(CustomMPTTModelAdmin):
    list_display_links = ('indented_name',)


class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'category', 'variants')
    list_display_links = ('name', )
    search_fields = ('name', )
    # exclude = ('unique',)
    # readonly_fields = ('unique',)


class AdvertAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ValueAdmin(admin.ModelAdmin):
    list_display = ('value',)

admin.site.register(Location, LocationMPTTModelAdmin)
admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Attribute, CategoryAttributeAdmin)
admin.site.register(AdvertsAdvert, AdvertAdmin)
admin.site.register(Value, ValueAdmin)
