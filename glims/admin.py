from django.contrib import admin
from models import EmailTemplate
from lims import Project, Sample, Experiment, ModelType, WorkflowTemplate,  WorkflowProcess#, ProjectType, ProjectTypePlugins
from forms import WorkflowTemplateForm, WorkflowProcessForm
from guardian.admin import GuardedModelAdmin
from  django.contrib.contenttypes.generic import GenericInlineModelAdmin, GenericStackedInline


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
class ProjectAdmin(GuardedModelAdmin):
    model = Project
#     inlines = [
#         FileInlineAdmin,
#     ]
class SampleAdmin(GuardedModelAdmin):
    model = Sample
class ExperimentAdmin(GuardedModelAdmin):
    model = Experiment
class ModelTypeAdmin(GuardedModelAdmin):
    model = ModelType

class WorkflowProcessInline(admin.TabularInline):
    model = WorkflowProcess
    form = WorkflowProcessForm
class WorkflowTemplateAdmin(admin.ModelAdmin):
    model = WorkflowTemplate
    form = WorkflowTemplateForm
    inlines = [
        WorkflowProcessInline,
    ]
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
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ModelType, ModelTypeAdmin)
admin.site.register(WorkflowTemplate, WorkflowTemplateAdmin)

