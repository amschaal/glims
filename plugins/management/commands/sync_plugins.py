from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string
from django.conf import settings
from plugins.models import Plugin

class Command(BaseCommand):
#     option_list = BaseCommand.option_list + (
# #         make_option('--long', '-l', dest='long',
# #             help='Help for the long options'),
#     )
    help = 'Synchronize plugin types included in PLUGINS setting'
    def handle(self, **options):
        PLUGINS = getattr(settings,'PLUGINS')
        for plugin_string in PLUGINS:
            plugin = import_string(plugin_string)
            try:
                obj = Plugin.objects.get(id=plugin.id)
                obj.name = plugin.name
                obj.description = plugin.description
                obj.save()
                print "Updated plugin: " + plugin.id
            except Plugin.DoesNotExist:
                values = {'id':plugin.id,'name':plugin.name,'description':plugin.description}
                obj = Plugin.objects.create(**values)
                print "Created plugin: " + plugin.id