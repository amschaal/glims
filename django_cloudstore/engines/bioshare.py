from django_cloudstore.engines import BaseStorageEngine
from django.conf import settings
import json, urllib2
import subprocess
class BioshareStorageEngine(BaseStorageEngine):
    ENGINE_ID = 'BIOSHARE'
    @staticmethod
    def create(name,description,attributes):
        from django_cloudstore.models import CloudStore
        cloudstore = CloudStore(storage_engine=BioshareStorageEngine.ENGINE_ID,name=name,description=description,attributes=attributes)
        req = urllib2.Request(settings.BIOSHARE_SETTINGS['CREATE_URL'])
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Token %s'%settings.BIOSHARE_SETTINGS['TOKEN'])
        filesystem = attributes['filesystem'] if attributes.has_key('filesystem') else settings.BIOSHARE_SETTINGS['DEFAULT_FILESYSTEM']
        params = {"name":name,"notes":description,"filesystem":filesystem}
        if attributes.has_key('link_to_path'):
            params['link_to_path'] = attributes['link_to_path']
        response = urllib2.urlopen(req, json.dumps(params))
        
        if response.getcode() == 200:
            data = json.load(response)
            cloudstore.attributes = data
            cloudstore.url = data['url']
            cloudstore.save()
            return cloudstore
#         curl -X POST https://bioshare.bioinformatics.ucdavis.edu/bioshare/api/shares/create/ -H 'Authorization: Token 891faf40003c7c7503c12654b9651ca713326556' -H 'Content-Type: application/json' -d '{"name":"xyz","notes":"xyz","filesystem":1,"link_to_path":"/home/adam/sdfsfd"}'
        #Do some stuff to create share
        
    def copy_path(self,from_path,to_path=""):
#         if self.cloudstore.attributes
        destination = "%s@%s:/%s/%s" % (settings.BIOSHARE_SETTINGS["RSYNC_USER"],settings.BIOSHARE_SETTINGS["HOST"],self.cloudstore.attributes['id'],to_path)
        subprocess.call(["rsync", "-vrzt", "--no-p", "--no-g", "--chmod=ugo=rwX", from_path, destination])
