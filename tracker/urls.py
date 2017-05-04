from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

from rest_framework import routers
from api import LogViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'logs', LogViewSet,'Log')
router.register(r'categories', CategoryViewSet,'Category')


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
)

