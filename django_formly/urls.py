from django.conf.urls import patterns, include, url
urlpatterns = patterns('',)


urlpatterns += patterns('',
    url(r'^form/(?P<key>[\-\w]+)/$', 'django_formly.views.get_formly_form', name='get_formly_form'),
)

