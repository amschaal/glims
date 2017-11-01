from django.conf.urls import url
from glims.samples import views


urlpatterns = [
    url(r'^template/download/$', views.sample_template, name='sample_template'),
    url(r'^samplesheet/(?P<project_id>\d+)/$', views.sample_sheet, name='download_samplesheet'),
    url(r'^import_samplesheet/(?P<project_id>\d+)/$', views.import_samplesheet, name='import_samplesheet'),
]

