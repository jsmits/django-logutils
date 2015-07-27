DEBUG = True

USE_TZ = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_logutils",
]

SITE_ID = 1

MIDDLEWARE_CLASSES = ()

SECRET_KEY = 'abcdef'
