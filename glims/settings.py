"""
Django settings for glims project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jn+=$cikt$$$*mazyt2bz!nvmfmx2_nyn62cp3nhnx=6h1=p_f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
COMPRESS_ENABLED = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_js_utils',
    'compressor',
    'glims.apps.GlimsConfig',
    'permissions',
    'attachments',
    'proteomics',
#     'bioinformatics',
    'plugins',
    'tasks',
    'guardian',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'crispy_forms',
    'django_extensions',
    'extensible',
    'django_compute',
    'autocomplete_light',
    'django_cloudstore',
    'notifications',
    'accounts',
    'logger',
    'bioshare',
    'afs.apps.AFSConfig',
    'sequencing',
    'tracker'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'notifications.middleware.NotificationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'glims.middlewares.ThreadLocal.ThreadLocalMiddleware',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "glims.context_processors.menus",
    "glims.context_processors.tab",
    "glims.context_processors.plugins",
    'notifications.context_processors.notifications'
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)
#Guardian setting
ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'glims.urls'

WSGI_APPLICATION = 'glims.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATIC_ROOT = os.path.join(BASE_DIR,'STATIC')

DJANGO_JSON_FORMS_UPLOAD_DIRECTORY = os.path.join(MEDIA_ROOT,'dynamic_uploads')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'glims.api.pagination.StandardPagePagination',
#     'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend','rest_framework.filters.OrderingFilter','rest_framework.filters.SearchFilter',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework_filters.backends.DjangoFilterBackend','rest_framework.filters.OrderingFilter','rest_framework.filters.SearchFilter','extensible.drf.filters.MultiFieldFilter'),
    'PAGE_SIZE': 10,
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 1000             # Maximum limit allowed when using `?page_size=xxx`.
}
PERMISSIONS_APP = {
    'manage_template': 'glims/manage_permissions.html',
    'manage_user_template' : 'glims/manage_user_permissions.html',
    'manage_group_template' : 'glims/manage_group_permissions.html',
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

COMPUTE_JOB_CALLBACKS = ['glims.callbacks.JOB_CALLBACKS']

SEARCHGUI_PATH = os.path.join(BASE_DIR,'proteomics/lib/SearchGUI/SearchGUI.jar')

# DJANGO_FORMLY_FORMS = {
#     'BioinfoProjectForm':{'form':'bioinformatics.forms.BioinfoProjectForm'},
#     'ProjectForm':{'form':'glims.forms.ProjectForm'}
# }

NOTIFICATION_TYPES = (
    'glims.notification_types.NOTIFICATION_TYPES',
)

NOTIFICATION_EMAIL_FREQUENCY_HOURS=1

ATTACHMENT_UPLOAD_TO_FUNCTION = 'glims.attachments_config.attachment_upload_to'

FILES_ROOT = MEDIA_ROOT

DIRECTORY_FUNCTIONS = {
    'get_project_directory':'glims.files.directories.get_project_directory',
    'create_project_directories':'glims.files.directories.create_project_directories',
    'get_group_lab_directory':'glims.files.directories.get_group_lab_directory',
    'get_lab_directory_name':'glims.files.directories.get_lab_directory_name',
    'get_sample_directory':'glims.files.directories.get_sample_directory',
}


from config import *