from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from proteomics import views
urlpatterns = patterns('',)

from rest_framework import routers
from proteomics.api.viewsets import FastaFileViewSet, ParameterFileViewSet

router = routers.DefaultRouter()
router.register(r'fasta_files', FastaFileViewSet)
router.register(r'parameter_files', ParameterFileViewSet)

urlpatterns += patterns('',
    url(r'^fasta_files/uniprot/$', 'proteomics.views.uniprot', name='proteomics__uniprot'),
    url(r'^fasta_files/$', 'proteomics.views.fasta_files', name='proteomics__fasta_files'),
    url(r'^fasta_files/create$', login_required(views.FastaFileCreate.as_view()), name='proteomics__create_fasta_file'),
    url(r'^fasta_files/create_from_url/$', 'proteomics.views.create_fasta_from_url', name='proteomics__create_fasta_from_url'),
    url(r'^fasta_files/(?P<pk>[\d]+)/update/$', login_required(views.FastaFileUpdate.as_view()), name='proteomics__update_fasta_file'),
    url(r'^fasta_files/(?P<pk>[\d]+)/details/$', 'proteomics.views.fasta_file', name='proteomics__fasta_file'),
    url(r'^fasta_files/(?P<pk>[\d]+)/view/$', 'proteomics.views.view_fasta', name='proteomics__view_fasta'),
    url(r'^parameter_files/$', 'proteomics.views.parameter_files', name='proteomics__parameter_files'),
    url(r'^parameter_files/create$', login_required(views.ParameterFileCreate.as_view()), name='proteomics__create_parameter_file'),
    url(r'^parameter_files/(?P<pk>[\d]+)/update/$', login_required(views.ParameterFileUpdate.as_view()), name='proteomics__update_parameter_file'),
    url(r'^searchcli/$', 'proteomics.views.searchcli', name='proteomics__searchcli'),
    url(r'^api/run_searchcli/$', 'proteomics.views.run_searchcli', name='proteomics__run_searchcli'),
    url(r'^api/', include(router.urls)),
)

