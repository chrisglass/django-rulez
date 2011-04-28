import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'rulez',
    'rulez.tests',
    )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'rulez.backends.ObjectPermissionBackend',
)

