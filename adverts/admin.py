from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from adverts.helpers.html_helper import get_mptt_indented_menu
from adverts.models import Region, Category, Attribute


class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_name')
    list_display_links = ('indented_name',)

    def indented_name(self, instance):
        return get_mptt_indented_menu(self, instance)

    indented_name.short_description = 'something nice'


class RegionMPTTModelAdmin(CustomMPTTModelAdmin):
    list_display_links = ('indented_name',)


class CategoryMPTTModelAdmin(CustomMPTTModelAdmin):
    list_display_links = ('indented_name',)


class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'category', 'variants')
    list_display_links = ('name', )
    search_fields = ('name', )


admin.site.register(Region, RegionMPTTModelAdmin)
admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Attribute, CategoryAttributeAdmin)
