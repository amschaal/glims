from django.conf.urls import patterns, include, url
urlpatterns = patterns('',)

from rest_framework import routers
from api import BioinfoProjectViewSet

router = routers.DefaultRouter()
router.register(r'bioinfo_projects', BioinfoProjectViewSet)

urlpatterns += patterns('',
    url(r'^projects/$', 'bioinformatics.views.bioinfo_projects', name='bioinformatics__projects'),
    url(r'^api/', include(router.urls)),
)

