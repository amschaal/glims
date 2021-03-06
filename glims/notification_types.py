from notifications.configuration import NotificationConfiguration

class NoteCreatedConf(NotificationConfiguration):
    name = 'Note created'
    description = 'Get notified when a note is written.'
    aggregable = True
    @classmethod
    def aggregated_text(cls,notifications):
        return "%s: There are %d new notes" % (str(notifications[0].content_object),len(notifications))
# class URLCreatedConf(NotificationConfiguration):
#     name = 'URL created'
#     description = 'Get notified when a URL is added to an order.'
#     aggregable = True
#     @classmethod
#     def aggregated_text(cls,user_notifications):
#         return "There are %d new URLs for you order" % len(user_notifications)
class FileCreatedConf(NotificationConfiguration):
    name = 'File uploaded'
    description = 'Get notified when a file is uploaded.'
    aggregable = True
    @classmethod
    def aggregated_text(cls,notifications):
        return "%s: %d new files have been uploaded" %  (str(notifications[0].content_object),len(notifications))
class ObjectUpdatedConf(NotificationConfiguration):
    name = 'Object updated'
    description = 'Get notified when an object has been updated.'
    aggregable = True
    @classmethod
    def aggregated_text(cls,notifications):
        return '"%s" has been updated %d times' %  (str(notifications[0].content_object),len(notifications))    

NOTIFICATION_TYPES = {
    'note_created': NoteCreatedConf,
    'file_created': FileCreatedConf,
    'object_updated': ObjectUpdatedConf
}