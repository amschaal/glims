from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

from rest_framework import routers
import api
import views

router = routers.DefaultRouter()
router.register(r'logs', api.LogViewSet,'Log')
router.register(r'categories', api.CategoryViewSet,'Category')
router.register(r'exports', api.ExportViewSet,'Export')


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^exports/$', views.exports, name='exports'),
)

