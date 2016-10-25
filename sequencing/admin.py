from django.contrib import admin
from sequencing.models import Machine, Run, Lane

admin.site.register(Machine)
admin.site.register(Run)
admin.site.register(Lane)

