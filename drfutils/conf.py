from django.conf import settings

TOKEN_HEADER = getattr(
    settings, 'DRF_UTILS_SERVICE_TOKEN_HEADER', 'X-Service-Access-Token'
)
