from django.contrib import admin
from models import EmailTemplate
from glims.models import Project, Sample, ModelType, Adapter
from guardian.admin import GuardedModelAdmin
from glims.models import Lab
from glims.models import Status


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


# class StatusAdmin(admin.ModelAdmin):
#     model = Status
# 
class StatusInline(admin.TabularInline):
    model = Status
    extra = 1

class ModelTypeAdmin(GuardedModelAdmin):
    model = ModelType
    inlines = [
        StatusInline,
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
admin.site.register(Adapter)
# admin.site.register(Status, StatusAdmin)

