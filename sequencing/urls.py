from django.conf.urls import include, url
from rest_framework import routers
from sequencing.api import views as api_views
import views

router = routers.DefaultRouter()
router.register(r'runs', api_views.RunViewSet,'Run')
router.register(r'machines', api_views.MachineViewSet,'Machine')

urlpatterns = [
    url(r'^runs/$', views.runs, name='runs'),
    url(r'^runs/(?P<pk>[\-\w]+)/$', views.run, name='run'),
    url(r'^api/', include(router.urls)),
]
