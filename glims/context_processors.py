from django.conf import settings
def menus(request):
    return {'menus':settings.MENUS}