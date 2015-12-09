import os


SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', '1234'
)

INSTALLED_APPS = (
    'rest_framework',
)
