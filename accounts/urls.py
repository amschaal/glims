from django.conf.urls import include, url
from rest_framework import routers
from api import AccountViewSet

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet,'Account')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]

