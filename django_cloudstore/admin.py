from django.contrib import admin
from django_cloudstore.models import CloudStore
# Register your models here.
class CloudStoreAdmin(admin.ModelAdmin):
    model = CloudStore

admin.site.register(CloudStore, CloudStoreAdmin)
