from django.conf.urls import url
import views

urlpatterns = [
    url(r'^form/(?P<key>[\-\w]+)/$', views.get_formly_form, name='get_formly_form'),
]

