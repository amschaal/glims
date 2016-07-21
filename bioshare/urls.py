from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

from rest_framework import routers
from api import ProjectShareViewSet

router = routers.DefaultRouter()
router.register(r'project_shares', ProjectShareViewSet,'ProjectShare')

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
)

