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

urlpatterns = patterns('',)
# if USE_CAS:
#     admin.site.login = login_required(admin.site.login)
#     urlpatterns += patterns('',
#         url(r'^login/$', 'cas.views.login', name='login'),
#         url(r'^logout/$', 'cas.views.logout', name='logout'),
#         url(r'^admin/logout/$', 'cas.views.logout'),
#     )

from rest_framework import routers
from api import ProjectViewSet, SampleViewSet, GroupViewSet, ModelTypeSerializerViewSet, PoolViewSet,WorkflowViewSet, JobViewset, JobSubmissionViewset

router = routers.DefaultRouter()
router.register(r'model_types', ModelTypeSerializerViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'samples', SampleViewSet)
router.register(r'pools', PoolViewSet)
router.register(r'workflows', WorkflowViewSet)
router.register(r'jobs', JobViewset)
router.register(r'submissions', JobSubmissionViewset)
router.register(r'groups', GroupViewSet)




urlpatterns += patterns('',
    # Examples:
#     url(r'^$', 'glims.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'glims.views.home', name='home'),
    url(r'^projects/(?P<pk>[\-\w]+)/$', 'glims.views.project', name='project'),
    url(r'^samples/(?P<pk>[\-\w]+)/$', 'glims.views.sample', name='sample'),
    url(r'^samples/(?P<pk>[\-\w]+)/update/$', login_required(glims_views.SampleUpdate.as_view()), name='update_sample'),
#     url(r'^file/(?P<pk>\d+)/get/$', 'glims.views.get_file', name='get_file'),
#     url(r'^files/(?P<model>\w+)/(?P<pk>[\-\w]+)/attach/$', 'glims.views.attach_file', name='attach_file'),
    url(r'^pis/$', 'glims.views.pis', name='pis'),
    url(r'^projects/$', 'glims.views.projects', name='projects'),
    url(r'^projects/create$', 'glims.views.create_project', name='create_project'),
    url(r'^projects/(?P<pk>[\-\w]+)/update/$', login_required(glims_views.ProjectUpdate.as_view()), name='update_project'),
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
    url(r'^job_submissions/$', 'glims.views.job_submissions', name='job_submissions'),
    url(r'^jobs/(?P<job_id>\d+\.?\d*)/$', 'glims.views.job', name='job'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^admin/model_types/$', 'glims.views.model_types', name='model_types'),
    url(r'^permissions/', include(permission_urls.urlpatterns)),
    url(r'^attachments/', include(attachment_urls.urlpatterns)),
    url(r'^proteomics/', include(proteomics_urls.urlpatterns)),
    url(r'^sample/(?P<pk>[\-\w]+)/$', 'glims.views.sample', name='sample'),
    url(r'^api/add_samples_to_cart/$', 'glims.api.add_samples_to_cart', name='add_samples_to_cart'),
    url(r'^api/remove_samples_from_cart/$', 'glims.api.remove_samples_from_cart', name='remove_samples_from_cart'),
    url(r'^api/', include(router.urls)),
    url(r'^jsurls.js$', 'utils.jsutils.jsurls', {}, 'jsurls'),
    url(r'^api/job/(?P<job_id>\d+\.?\d*)/update/$', 'glims.api.update_job', name='update_job'),
    url(r'^api/pool/(?P<pk>\d+)/update/$', 'glims.api.update_pool', name='update_pool'),
    url(r'^api/pool/(?P<pool_id>\d+)/sample/(?P<sample_id>\d+)/update/$', 'glims.api.update_pool_sample', name='update_pool_sample'),
    url(r'^api/pool/(?P<pk>\d+)/remove_samples/$', 'glims.api.remove_pool_samples', name='remove_pool_samples'),
    url(r'^api/pool/(?P<pk>\d+)/add_samples/$', 'glims.api.add_pool_samples', name='add_pool_samples'),

    url(r'^api/workflow/(?P<pk>\d+)/update/$', 'glims.api.update_workflow', name='update_workflow'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 