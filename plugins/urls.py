from django.conf.urls import url, include
from rest_framework import routers
from plugins.viewsets import ModelTypePluginViewset, PluginViewset
import api

router = routers.DefaultRouter()
router.register(r'model_type_plugins', ModelTypePluginViewset,'ModelTypePlugin')
router.register(r'plugins', PluginViewset,'Plugin')

urlpatterns = [
    
    url(r'^api/get_plugins/$', api.get_plugins, name='get_plugins'),
    url(r'^api/model_type/(?P<pk>\d+)/available_plugins/$', api.available_model_type_plugins, name='available_model_type_plugins'),
    url(r'^api/content_type/(?P<content_type>\d+)/object/(?P<pk>\d+)/plugins/$', api.object_plugins, name='object_plugins'),
    url(r'^api/', include(router.urls)),
]

