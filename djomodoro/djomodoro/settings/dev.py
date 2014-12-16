from .base import *

SECRET_KEY = 'jgge=u2_#8&$l)2y@10ss7_z12^@q@xkm-&yo%d^+=de!)6oc%'
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'djomodoro.db'),
    }
}