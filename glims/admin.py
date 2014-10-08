from django.contrib import admin
from models import EmailTemplate
# Register your models here.

class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate
admin.site.register(EmailTemplate, EmailTemplateAdmin)