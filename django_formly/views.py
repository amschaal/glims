from django.shortcuts import render
from django.template.context import RequestContext
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.module_loading import import_string
from django_formly.utils import generate_formly_fields


def get_formly_form(request,key):
    forms = settings.DJANGO_FORMLY_FORMS
    if not forms.has_key(key):
        return JsonResponse({'status':'error','message':'Unable to find form "%s"'%key},status=400)
    try:
        form = import_string(settings.DJANGO_FORMLY_FORMS[key]['form'])
        formly_form = generate_formly_fields(form())
        return JsonResponse({'fields':formly_form})
    except Exception, e:
        return JsonResponse({'status':'error','message': e.message})
