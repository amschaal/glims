from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)
# if USE_CAS:
#     admin.site.login = login_required(admin.site.login)
#     urlpatterns += patterns('',
#         url(r'^login/$', 'cas.views.login', name='login'),
#         url(r'^logout/$', 'cas.views.logout', name='logout'),
#         url(r'^admin/logout/$', 'cas.views.logout'),
#     )

from rest_framework import routers
from api import NoteViewSet

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet)


urlpatterns = patterns('',
    # Examples:
#     url(r'^$', 'glims.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^file/(?P<pk>\d+)/get/$', 'attachments.views.get_file', name='get_file'),
    url(r'^files/(?P<model>\w+)/(?P<pk>[\-\w]+)/attach/$', 'attachments.views.attach_file', name='attach_file'),
    url(r'^api/', include(router.urls)),
)

