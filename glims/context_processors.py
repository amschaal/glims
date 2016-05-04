from django.conf import settings
def menus(request):
    return {'menus':settings.MENUS}
def tab(request):
    return {'tab':request.GET.get('tab','')}

def plugins(request):
    from django.utils.module_loading import import_string
    css = []
    js = []
    css_unique = []
    js_unique = []
#     return {'plugins':{'css':css,'js':settings.PLUGINS}}
    for p in settings.PLUGINS:
        p = import_string(p)
        css += p.css_files
        js += p.js_files

    for c in css:
        if c not in css_unique:
            css_unique.append(c)
    for j in js:
        if j not in js_unique:
            js_unique.append(j)
    return {'plugins':{'css':css_unique,'js':js_unique}}