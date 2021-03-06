from django.conf.urls import include, url
from rest_framework import routers
import api
import views

router = routers.DefaultRouter()
router.register(r'logs', api.LogViewSet,'Log')
router.register(r'categories', api.CategoryViewSet,'Category')
router.register(r'exports', api.ExportViewSet,'Export')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^exports/$', views.exports, name='exports'),
    url(r'^project_report/$', views.project_report, name='project_report'),
]

