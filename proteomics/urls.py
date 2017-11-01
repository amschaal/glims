from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from proteomics import views
from proteomics.views import MZMLBrowser

from rest_framework import routers
from proteomics.api.viewsets import FastaFileViewSet, ParameterFileViewSet

router = routers.DefaultRouter()
router.register(r'fasta_files', FastaFileViewSet)
router.register(r'parameter_files', ParameterFileViewSet)

urlpatterns = [
    url(r'^fasta_files/uniprot/$', views.uniprot, name='proteomics__uniprot'),
    url(r'^fasta_files/$', views.fasta_files, name='proteomics__fasta_files'),
    url(r'^fasta_files/create$', login_required(views.FastaFileCreate.as_view()), name='proteomics__create_fasta_file'),
    url(r'^fasta_files/create_from_url/$', views.create_fasta_from_url, name='proteomics__create_fasta_from_url'),
    url(r'^fasta_files/(?P<pk>[\d]+)/update/$', login_required(views.FastaFileUpdate.as_view()), name='proteomics__update_fasta_file'),
    url(r'^fasta_files/(?P<pk>[\d]+)/details/$', views.fasta_file, name='proteomics__fasta_file'),
    url(r'^fasta_files/(?P<pk>[\d]+)/view/$', views.view_fasta, name='proteomics__view_fasta'),
    url(r'^parameter_files/$', views.parameter_files, name='proteomics__parameter_files'),
    url(r'^parameter_files/create$', login_required(views.ParameterFileCreate.as_view()), name='proteomics__create_parameter_file'),
    url(r'^parameter_files/(?P<pk>[\d]+)/update/$', login_required(views.ParameterFileUpdate.as_view()), name='proteomics__update_parameter_file'),
    url(r'^browse/mzml/$', MZMLBrowser.as_view(), name='browse_mzml'),
    url(r'^searchcli/$', views.searchcli, name='proteomics__searchcli'),
    url(r'^api/run_searchcli/$', views.run_searchcli, name='proteomics__run_searchcli'),
    url(r'^api/', include(router.urls)),
]

