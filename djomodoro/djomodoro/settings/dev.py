from .base import *

SECRET_KEY = 'jgge=u2_#8&$l)2y@10ss7_z12^@q@xkm-&yo%d^+=de!)6oc%'
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'djomodoro.db'),
    }
}

INTERNAL_IPS = (
    "127.0.0.1",
)

DEV_APPS = (
    'debug_toolbar',
)

DEV_MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += DEV_APPS
MIDDLEWARE_CLASSES = DEV_MIDDLEWARE + MIDDLEWARE_CLASSES # DDT first