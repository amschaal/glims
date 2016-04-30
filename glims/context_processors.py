from django.conf import settings
def menus(request):
    return {'menus':settings.MENUS}
def tab(request):
    return {'tab':request.GET.get('tab','')}

def plugins(request):
    from django.utils.module_loading import import_string
    css = []
    js = []
#     return {'plugins':{'css':css,'js':settings.PLUGINS}}
    for p in settings.PLUGINS:
        p = import_string(p)
        css += p.css_files
        js += p.js_files
    return {'plugins':{'css':css,'js':js}}