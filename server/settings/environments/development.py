import socket

from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from server.settings.components.rest_framework import REST_FRAMEWORK

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]

INSTALLED_APPS += (
    # Better debug:
    'debug_toolbar',
    'django_nose',
)

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        '{0}.1'.format(ip[:ip.rfind('.')])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ['127.0.0.1']

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = DEFAULT_RENDERER_CLASSES
