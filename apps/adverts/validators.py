from django.core.exceptions import ValidationError

from apps.adverts.models import Attribute

# dont work!!!

def attribute_name_validator(value):
    attributes = Attribute.objects.select_related('category').filter(name=value)
    # attributes_id = [attr.id for attr in attributes]
    # categories = Category.objects.filter(attribute_set__in=attributes_id)
    l = False
    for attr in attributes:
        attrs_in_cat = [attrib.name for attrib in attr.category.all_attributes()]
        print(attrs_in_cat)
        for name in attrs_in_cat:
            if value == name:
                l = True
                break
            else:
                # for child in attr.category.get_ancestors():
                #     for item in child.attribute_set.all():
                l = False
                continue
    print(l)
    if l:
        raise ValidationError(
            '%(value)s is not an even number',
            params={'value': value},
        )


