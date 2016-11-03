from django.conf.urls import patterns, include, url
from glims.samples import views


urlpatterns = patterns('',
    url(r'^template/download/$', 'glims.samples.views.sample_template', name='sample_template'),
    url(r'^samplesheet/(?P<project_id>\d+)/$', 'glims.samples.views.sample_sheet', name='download_samplesheet'),
    url(r'^import_samplesheet/(?P<project_id>\d+)/$', 'glims.samples.views.import_samplesheet', name='import_samplesheet'),
#     url(r'^create$', 'glims.samples.views.create_sample', name='create_sample_view'),
#     url(r'^api_create/$', 'glims.samples.views.create_update_sample', name='create_sample'),
#     url(r'^api_update/$', 'glims.samples.views.create_update_sample', name='update_sample'),
#     url(r'^samples/(?P<pk>[\-\w]+)/update/$', views.SampleUpdate.as_view(), name='update_sample'),
)

