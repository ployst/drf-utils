from rest_framework.test import APIRequestFactory

from ..models import Token
from ..permissions import HTTP_TOKEN_LOOKUP


class CoreApiClientTestMixin(object):
    """
    Mixin that creates a token to allow unlimited API access.
    """

    @classmethod
    def setUpClass(cls):
        cls.token = Token.objects.create()
        cls.request_factory = APIRequestFactory()

    @classmethod
    def tearDownClass(cls):
        Token.objects.all().delete()

    def get_token_headers(self):
        return {HTTP_TOKEN_LOOKUP: self.token.key}
