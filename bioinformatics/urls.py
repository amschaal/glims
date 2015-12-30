from django.conf.urls import patterns, include, url
urlpatterns = patterns('',)

from rest_framework import routers
from api import BioinfoProjectViewSet

router = routers.DefaultRouter()
router.register(r'bioinfo_projects', BioinfoProjectViewSet)

urlpatterns += patterns('',
    url(r'^projects/$', 'bioinformatics.views.bioinfo_projects', name='bioinformatics__projects'),
    url(r'^projects/(?P<pk>[\-\w]+)/$', 'bioinformatics.views.bioinfo_project', name='bioinformatics__project'),
    url(r'^projects/(?P<pk>[\-\w]+)/modify/$', 'bioinformatics.views.modify_bioinfo_project', name='modify_bioinformatics__project'),
    url(r'^api/', include(router.urls)),
)

