from django.conf.urls import patterns, include, url

urlpatterns = patterns('',)

from rest_framework import routers
from api import LogViewSet

router = routers.DefaultRouter()
router.register(r'logs', LogViewSet,'Log')


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
)

