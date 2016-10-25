from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'runs', views.RunViewSet,'Run')
router.register(r'machines', views.MachineViewSet,'Machine')

urlpatterns = patterns('',
    url(r'^runs/$', 'sequencing.views.runs', name='runs'),
    url(r'^runs/(?P<pk>[\-\w]+)/$', 'sequencing.views.run', name='run'),
    url(r'^api/', include(router.urls)),
)
