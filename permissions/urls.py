from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^(?P<model>\w+)/(?P<pk>[\-\w]+)/$', 'permissions.views.manage_permissions', name='permissions'),
    url(r'^(?P<model>\w+)/(?P<pk>[\-\w]+)/user/(?P<user_id>\d+)/$', 'permissions.views.manage_user_permissions', name='user_permissions'),
    url(r'^(?P<model>\w+)/(?P<pk>[\-\w]+)/group/(?P<group_id>\d+)/$', 'permissions.views.manage_group_permissions', name='group_permissions'),
)