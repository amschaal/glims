from django.conf import settings
def menus(request):
    return {'menus':settings.MENUS}
def tab(request):
    return {'tab':request.GET.get('tab','')}