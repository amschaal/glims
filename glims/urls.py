from django.conf.urls import patterns, include, url
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
from api import ProjectViewSet, SampleViewSet, ExperimentViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'samples', SampleViewSet)
router.register(r'experiments', ExperimentViewSet)
# router.register(r'notes', NoteViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns += patterns('',
    # Examples:
#     url(r'^$', 'glims.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'glims.views.home', name='home'),
    url(r'^project/(?P<pk>[\-\w]+)/$', 'glims.views.project', name='project'),
    url(r'^sample/(?P<pk>[\-\w]+)/$', 'glims.views.sample', name='sample'),
    url(r'^sample/(?P<pk>[\-\w]+)/update/$', glims_views.SampleUpdate.as_view(), name='update_sample'),
    url(r'^experiment/(?P<pk>[\-\w]+)/$', 'glims.views.experiment', name='experiment'),
#     url(r'^file/(?P<pk>\d+)/get/$', 'glims.views.get_file', name='get_file'),
#     url(r'^files/(?P<model>\w+)/(?P<pk>[\-\w]+)/attach/$', 'glims.views.attach_file', name='attach_file'),
    url(r'^pis/$', 'glims.views.pis', name='pis'),
    url(r'^projects/$', 'glims.views.projects', name='projects'),
    url(r'^projects/create$', 'glims.views.create_project', name='create_project'),
    url(r'^projects/(?P<pk>[\-\w]+)/update/$', glims_views.ProjectUpdate.as_view(), name='update_project'),
    url(r'^samples/$', 'glims.views.samples', name='samples'),
    url(r'^samples/create$', 'glims.views.create_sample', name='create_sample'),
    url(r'^experiments/$', 'glims.views.experiments', name='experiments'),
    url(r'^experiments/create$', 'glims.views.create_experiment', name='create_experiment'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^permissions/', include(permission_urls.urlpatterns)),
    url(r'^attachments/', include(attachment_urls.urlpatterns)),
    url(r'^proteomics/', include(proteomics_urls.urlpatterns)),
    url(r'^api/', include(router.urls)),
    url(r'^jsurls.js$', 'utils.jsutils.jsurls', {}, 'jsurls'),
)

