# {% load content_type %}
# {% with instance|content_type as ctype %}
#     <input type="hidden" name="content_type" value="{{ ctype.pk }}">
# {% endwith %}


from django import template
register = template.Library()
from django.contrib.contenttypes.models import ContentType

@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)
@register.filter
def content_type_id(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj).id

