from django.conf.urls import include, url

from rest_framework import routers
from api import LogViewSet

router = routers.DefaultRouter()
router.register(r'logs', LogViewSet,'Log')


urlpatterns = [
    url(r'^api/', include(router.urls)),
]

