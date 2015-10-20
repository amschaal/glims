from django.conf.urls import patterns, include, url
from glims.samples import views


urlpatterns = patterns('',
    url(r'^tsv_template/download/$', 'glims.samples.views.sample_template_tsv', name='sample_template_tsv'),
    url(r'^import_tsv/(?P<project_id>\d+)/$', 'glims.samples.views.import_tsv_samples', name='import_tsv_samples'),
    url(r'^api_create/$', 'glims.samples.views.create_update_sample', name='create_sample'),
    url(r'^api_update/$', 'glims.samples.views.create_update_sample', name='update_sample'),
    url(r'^samples/(?P<pk>[\-\w]+)/update/$', views.SampleUpdate.as_view(), name='update_sample'),
)

