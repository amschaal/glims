from django.contrib import admin
from models import EmailTemplate
from lims import Project, Sample, ModelType
from guardian.admin import GuardedModelAdmin
from  django.contrib.contenttypes.generic import GenericInlineModelAdmin, GenericStackedInline
from glims.lims import Lab
from glims.models import Status, StatusOption


class PostAdmin(GuardedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

# class FileInlineAdmin(GenericStackedInline):
#     model = File
class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate
# class PluginsInline(admin.TabularInline):
#     model = ProjectTypePlugins
#     extra = 1
class LabAdmin(GuardedModelAdmin):
    model = Lab
class ProjectAdmin(GuardedModelAdmin):
    model = Project
#     inlines = [
#         FileInlineAdmin,
#     ]
class SampleAdmin(GuardedModelAdmin):
    model = Sample


class StatusAdmin(admin.ModelAdmin):
    model = Status

class StatusOptionsInline(admin.TabularInline):
    model = StatusOption
    extra = 1

class ModelTypeAdmin(GuardedModelAdmin):
    model = ModelType
    inlines = [
        StatusOptionsInline,
    ]
# 
# class StatusOptionsInline(GuardedModelAdmin):
#     model = ProjectType
#     inlines = [
#         PluginsInline,
#     ]

# class ProjectTypeAdmin(GuardedModelAdmin):
#     model = ProjectType
#     inlines = [
#         PluginsInline,
#     ]

# class ProjectTypeAdmin(GuardedModelAdmin):
#     model = ProjectType
#     inlines = [
#         PluginsInline,
#     ]

admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(ModelType, ModelTypeAdmin)
admin.site.register(Status, StatusAdmin)

