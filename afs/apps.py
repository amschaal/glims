from django.apps import AppConfig

class AFSConfig(AppConfig):
    name = 'afs'
    verbose_name = "AFS"
    def ready(self):
        print "AFS ready!!!!!!!"
#         raise Exception("WTF")
        from signals import handlers