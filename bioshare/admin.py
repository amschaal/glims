from django.contrib import admin
from bioshare.models import BioshareAccount


# class LabShareAdmin(admin.ModelAdmin):
#     model = LabShare

admin.site.register(BioshareAccount)

