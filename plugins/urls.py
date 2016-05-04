from django.conf.urls import patterns, url, include
from rest_framework import routers
from plugins.viewsets import ModelTypePluginViewset, PluginViewset

router = routers.DefaultRouter()
router.register(r'model_type_plugins', ModelTypePluginViewset,'ModelTypePlugin')
router.register(r'plugins', PluginViewset,'Plugin')

urlpatterns = patterns('',
    
    url(r'^api/get_plugins/$', 'plugins.api.get_plugins', name='get_plugins'),
    url(r'^api/model_type/(?P<pk>\d+)/available_plugins/$', 'plugins.api.available_model_type_plugins', name='available_model_type_plugins'),
    url(r'^api/', include(router.urls)),

)

