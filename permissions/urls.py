from django.conf.urls import url
import views

urlpatterns = [
    url(r'^(?P<model>\w+)/(?P<pk>[\-\w]+)/$', views.manage_permissions, name='permissions'),
    url(r'^(?P<model>\w+)/(?P<pk>[\-\w]+)/user/(?P<user_id>\d+)/$', views.manage_user_permissions, name='user_permissions'),
    url(r'^(?P<model>\w+)/(?P<pk>[\-\w]+)/group/(?P<group_id>\d+)/$', views.manage_group_permissions, name='group_permissions'),
]