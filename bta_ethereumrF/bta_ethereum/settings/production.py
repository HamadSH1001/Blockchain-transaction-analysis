from .base import *

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    ALLOWED_HOSTS = ["*"]
