from django.conf import settings
CREATE_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/api/shares/create/'
VIEW_URL = settings.BIOSHARE_SETTINGS['URL'] + '/bioshare/view/{id}/'