from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from glims import views as glims_views
from django.contrib import admin
admin.autodiscover()
from permissions import urls as permission_urls
from attachments import urls as attachment_urls
from proteomics import urls as proteomics_urls
from django_json_forms import urls as json_form_urls
from extensible import urls as extensible_urls
from django_compute import urls as compute_urls
import glims
urlpatterns = patterns('',)
# if USE_CAS:
#     admin.site.login = login_required(admin.site.login)
#     urlpatterns += patterns('',
#         url(r'^login/$', 'cas.views.login', name='login'),
#         url(r'^logout/$', 'cas.views.logout', name='logout'),
#         url(r'^admin/logout/$', 'cas.views.logout'),
#     )

from rest_framework import routers
from api import ProjectViewSet, SampleViewSet, LabViewSet, ModelTypeSerializerViewSet, PoolViewSet,WorkflowViewSet, JobViewset,  FormView

router = routers.DefaultRouter()
router.register(r'model_types', ModelTypeSerializerViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'samples', SampleViewSet)
router.register(r'pools', PoolViewSet)
router.register(r'workflows', WorkflowViewSet)
router.register(r'jobs', JobViewset)
# router.register(r'submissions', JobSubmissionViewset)
router.register(r'labs', LabViewSet)




urlpatterns += patterns('',
    # Examples:
#     url(r'^$', 'glims.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'glims.views.home', name='home'),
    url(r'^projects/(?P<pk>[\-\w]+)/$', 'glims.views.project', name='project'),
#     url(r'^samples/(?P<pk>[\-\w]+)/$', 'glims.views.sample', name='sample'),
#     url(r'^samples/(?P<pk>[\-\w]+)/update/$', login_required(glims_views.SampleUpdate.as_view()), name='update_sample'),
#     url(r'^file/(?P<pk>\d+)/get/$', 'glims.views.get_file', name='get_file'),
#     url(r'^files/(?P<model>\w+)/(?P<pk>[\-\w]+)/attach/$', 'glims.views.attach_file', name='attach_file'),
    url(r'^labs/$', 'glims.views.labs', name='labs'),
    url(r'^labs/create$', 'glims.views.create_lab', name='create_lab'),
    url(r'^labs/(?P<pk>\d+)/$', 'glims.views.lab', name='lab'),
    url(r'^projects/$', 'glims.views.projects', name='projects'),
    url(r'^projects/create/choose_type/$', 'glims.views.choose_project_type', name='choose_project_type'),
    url(r'^projects/create$', 'glims.views.create_project', name='create_project'),
    url(r'^projects/(?P<pk>[\-\w]+)/update/$', 'glims.views.create_project', name='update_project'),
    url(r'^samples/$', 'glims.views.samples', name='samples'),
    url(r'^samples/create$', 'glims.views.create_sample', name='create_sample'),
    url(r'^pools/$', 'glims.views.pools', name='pools'),
    url(r'^pools/create$', 'glims.views.create_pool', name='create_pool'),
    url(r'^pools/(?P<pk>[\-\w]+)/$', 'glims.views.pool', name='pool'),
    url(r'^pools/(?P<pk>[\-\w]+)/delete/$', 'glims.views.delete_pool', name='delete_pool'),
    url(r'^cart/$', 'glims.views.cart', name='cart'),
#     url(r'^workflow/$', 'glims.views.workflow', name='workflow'),
    url(r'^workflows/$', 'glims.views.workflows', name='workflows'),
    url(r'^workflows/(?P<pk>[\d]+)/$', 'glims.views.workflow', name='workflow'),
    url(r'^workflows/create/$', 'glims.views.create_workflow', name='create_workflow'),
    url(r'^process/(?P<pk>[\d]+)/update/$', FormView.as_view(model=glims.lims.Process,form_class=glims.forms.ProcessForm), name='update_process'),
    
    url(r'^jobs/$', 'glims.views.jobs', name='jobs'),
#     url(r'^job_submissions/(?P<id>[\d_A-Za-z]+)/$', 'glims.views.job_submission', name='job_submission'),
    url(r'^jobs/(?P<id>[A-Z0-9]{10})/$', 'glims.views.job', name='job'),
    url(r'^jobs/(?P<id>[A-Z0-9]{10})/files/$', 'glims.views.job_files', name='job_files'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^admin/model_types/$', 'glims.views.model_types', name='model_types'),
    url(r'^admin/model_types/(?P<pk>\d+)/$', 'glims.views.model_type', name='model_type'),
    url(r'^permissions/', include(permission_urls.urlpatterns)),
    url(r'^attachments/', include(attachment_urls.urlpatterns)),
    url(r'^proteomics/', include(proteomics_urls.urlpatterns)),
    url(r'^sample/(?P<pk>[\-\w]+)/$', 'glims.views.sample', name='sample'),
    url(r'^api/add_samples_to_cart/$', 'glims.api.add_samples_to_cart', name='add_samples_to_cart'),
    url(r'^api/remove_samples_from_cart/$', 'glims.api.remove_samples_from_cart', name='remove_samples_from_cart'),
    url(r'^api/', include(router.urls)),
    url(r'^jsurls.js$', 'utils.jsutils.jsurls', {}, 'jsurls'),
#    url(r'^api/job/(?P<job_id>\d+\.?\d*)/update/$', 'glims.api.update_job', name='update_job'),
    url(r'^api/pool/(?P<pk>\d+)/update/$', 'glims.api.update_pool', name='update_pool'),
    url(r'^api/pool/(?P<pool_id>\d+)/sample/(?P<sample_id>\d+)/update/$', 'glims.api.update_pool_sample', name='update_pool_sample'),
    url(r'^api/pool/(?P<pk>\d+)/remove_samples/$', 'glims.api.remove_pool_samples', name='remove_pool_samples'),
    url(r'^api/pool/(?P<pk>\d+)/add_samples/$', 'glims.api.add_pool_samples', name='add_pool_samples'),

    url(r'^api/workflow/(?P<pk>\d+)/update/$', 'glims.api.update_workflow', name='update_workflow'),
    url(r'^samples/', include('glims.samples.urls')),
    url(r'^json_forms/', include(json_form_urls.urlpatterns)),
    url(r'^extensible/', include(extensible_urls.urlpatterns)),
    url(r'^compute/', include(compute_urls.urlpatterns)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 