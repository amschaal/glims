
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jn+=$cikt$$$*mazyt2bz!nvmfmx2_nyn62cp3nhnx=6h1=p_f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'glims',
        'USER': 'glims',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LAB_DATA_DIRECTORY = os.path.join(BASE_DIR,'data','labs')

ADMIN_EMAIL = 'admin@site.com'

SENDFILE_BACKEND = 'sendfile.backends.development'

MENUS = (
    'proteomics/menu.html',
    'bioinformatics/menu.html',
)
BIOCORE_ID = 1