from django import template


register = template.Library()


@register.filter
def advert_attribute_value(instance, attr_id):
    value = instance.get_value(attr_id)
    return value