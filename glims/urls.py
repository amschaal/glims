from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from glims import views
from django.contrib import admin
from plugins.utils import PluginManager
from bioshare import urls as bioshare_urls
admin.autodiscover()
from permissions import urls as permission_urls
from attachments import urls as attachment_urls
from proteomics import urls as proteomics_urls
from extensible import urls as extensible_urls
from django_compute import urls as compute_urls
from django_formly import urls as formly_urls
from notifications import urls as notification_urls
import api
from utils.jsutils import jsurls
from django.contrib.auth import views as auth_views
# if USE_CAS:
#     admin.site.login = login_required(admin.site.login)
#     urlpatterns += patterns('',
#         url(r'^login/$', 'cas.views.login, name='login'),
#         url(r'^logout/$', 'cas.views.logout, name='logout'),
#         url(r'^admin/logout/$', 'cas.views.logout'),
#     )

from rest_framework import routers
from glims.api.viewsets import ProjectViewSet, SampleViewSet, LabViewSet, ModelTypeSerializerViewSet, PoolViewSet, JobViewset, UserViewSet, GroupViewSet,\
    StatusSerializerViewSet, AdapterViewSet, LibraryViewSet,\
    ModelSubTypeSerializerViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet,'User')
router.register(r'groups', GroupViewSet,'Group')
router.register(r'model_types', ModelTypeSerializerViewSet,'ModelType')
router.register(r'model_subtypes', ModelSubTypeSerializerViewSet,'ModelSubType')
router.register(r'projects', ProjectViewSet,'Project')
router.register(r'samples', SampleViewSet,'Sample')
router.register(r'adapters', AdapterViewSet,'Adapter')
router.register(r'libraries', LibraryViewSet,'Library')
router.register(r'pools', PoolViewSet,'Pool')
router.register(r'jobs', JobViewset,'Job')
# router.register(r'submissions', JobSubmissionViewset)
router.register(r'labs', LabViewSet,'Lab')
router.register(r'statuses', StatusSerializerViewSet,'Status')

urlpatterns = [
    # Examples:
#     url(r'^$', views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.home, name='home'),
    url(r'^projects/(?P<pk>[\-\w]+)/$', views.project, name='project'),
#     url(r'^samples/(?P<pk>[\-\w]+)/$', views.sample, name='sample'),
#     url(r'^samples/(?P<pk>[\-\w]+)/update/$', login_required(glims_views.SampleUpdate.as_view()), name='update_sample'),
#     url(r'^file/(?P<pk>\d+)/get/$', views.get_file, name='get_file'),
#     url(r'^files/(?P<model>\w+)/(?P<pk>[\-\w]+)/attach/$', views.attach_file, name='attach_file'),
    url(r'^labs/$', views.labs, name='labs'),
    url(r'^labs/(?P<pk>\d+)/modify/$', views.modify_lab, name='modify_lab'),
    url(r'^labs/create$', views.create_lab, name='create_lab'),
    url(r'^labs/(?P<pk>\d+)/$', views.lab, name='lab'),
    url(r'^projects/$', views.projects, name='projects'),
#     url(r'^projects/(?P<pk>[\-\w]+)/data/$', views.project_files, name='project_files'),
    url(r'^samples/$', views.samples, name='samples'),
    url(r'^pools/$', views.pools, name='pools'),
#     url(r'^pools/create$', views.create_pool, name='create_pool'),
    url(r'^pools/(?P<pk>[\-\w]+)/$', views.pool, name='pool'),
    url(r'^pools/(?P<pk>[\-\w]+)/delete/$', views.delete_pool, name='delete_pool'),
    url(r'^cart/$', views.cart, name='cart'),
#     url(r'^workflow/$', views.workflow, name='workflow'),
    
    url(r'^jobs/$', views.jobs, name='jobs'),
#     url(r'^job_submissions/(?P<id>[\d_A-Za-z]+)/$', views.job_submission, name='job_submission'),
    url(r'^jobs/(?P<id>[A-Z0-9]{10})/$', views.job, name='job'),
    url(r'^jobs/(?P<id>[A-Z0-9]{10})/files/$', views.job_files, name='job_files'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html','redirect_authenticated_user': True}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'registration/logout.html','next_page':'home'}, name='logout'),
    url(r'^admin/model_types/$', views.model_types, name='model_types'),
    url(r'^admin/model_types/(?P<pk>\d+)/$', views.model_type, name='model_type'),
    url(r'^permissions/', include(permission_urls.urlpatterns)),
    url(r'^attachments/', include(attachment_urls.urlpatterns)),
    url(r'^proteomics/', include(proteomics_urls.urlpatterns)),
#     url(r'^bioinformatics/', include(bioinformatics_urls.urlpatterns)),
    url(r'^sample/(?P<pk>[\-\w]+)/$', views.sample, name='sample'),
    url(r'^api/add_samples_to_cart/$', api.views.add_samples_to_cart, name='add_samples_to_cart'),
    url(r'^api/remove_samples_from_cart/$', api.views.remove_samples_from_cart, name='remove_samples_from_cart'),
    url(r'^api/', include(router.urls)),
    url(r'^jsurls.js$', jsurls, {}, 'jsurls'),
#    url(r'^api/job/(?P<job_id>\d+\.?\d*)/update/$', api.views.update_job, name='update_job'),
    url(r'^api/pool/(?P<pk>\d+)/update/$', api.views.update_pool, name='update_pool'),
    url(r'^api/pool/(?P<pool_id>\d+)/sample/(?P<sample_id>\d+)/update/$', api.views.update_pool_sample, name='update_pool_sample'),
    url(r'^api/pool/(?P<pk>\d+)/remove_libraries/$', api.views.remove_pool_libraries, name='remove_pool_libraries'),
    url(r'^api/pool/(?P<pk>\d+)/add_libraries/$', api.views.add_pool_libraries, name='add_pool_libraries'),
    url(r'^api/projects/(?P<project_id>[\-\w]+)/data/(?:(?P<path>.*/))?$', api.views.project_files, name='get_project_files'),
    url(r'^samples/', include('glims.samples.urls')),
    url(r'^plugins/', include('plugins.urls')),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^extensible/', include(extensible_urls.urlpatterns)),
    url(r'^compute/', include(compute_urls.urlpatterns)),
    url(r'^formly_forms/', include(formly_urls.urlpatterns)),
    url(r'^notifications/', include(notification_urls.urlpatterns)),
    url(r'^bioshare/', include(bioshare_urls.urlpatterns)),
    url(r'^sequencing/', include('sequencing.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

plugin_manager = PluginManager()
urlpatterns += plugin_manager.get_urls()

 