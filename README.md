# DRF Utils

Utilities for Django Rest Framework we use at :ployst, including:

- Fields
- Serializer mixins
- Decorators

DRF Utils only supports Python 3. It has been tested with Python 3.4.

## Development

Run tests with:

    DJANGO_SETTINGS_MODULE=drfutils.tests.settings django-admin test

## Releasing

Circle takes care of releasing to PyPI. Simply create a tag in the form
3.2.1 and circle will build and release as 3.2.1.

To release locally, run `./release.sh <version>`
