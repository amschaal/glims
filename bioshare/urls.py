from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from api import ProjectShareViewSet

router = routers.DefaultRouter()
router.register(r'project_shares', ProjectShareViewSet,'ProjectShare')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]

