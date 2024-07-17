from .base import *

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
