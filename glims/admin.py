from django.contrib import admin
from models import EmailTemplate
from lims import Study, Sample, Experiment
from guardian.admin import GuardedModelAdmin


class PostAdmin(GuardedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


class EmailTemplateAdmin(admin.ModelAdmin):
    model = EmailTemplate
class StudyAdmin(GuardedModelAdmin):
    model = Study
class SampleAdmin(GuardedModelAdmin):
    model = Sample
class ExperimentAdmin(GuardedModelAdmin):
    model = Experiment

admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Experiment, ExperimentAdmin)