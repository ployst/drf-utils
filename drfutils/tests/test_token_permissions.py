from unittest import TestCase

from ..permissions import ClientTokenPermission, TOKEN_HEADER
from .mixins import CoreApiClientTestMixin


class TestTokenPermissions(CoreApiClientTestMixin, TestCase):

    def test_no_token_no_permission(self):
        request = self.request_factory.get('/')
        permissions = ClientTokenPermission()
        self.assertFalse(permissions.has_permission(request, None))
        self.assertFalse(request.has_valid_token)

    def test_valid_token_in_url_has_permission(self):
        request = self.request_factory.get('/', {TOKEN_HEADER: self.token.key})
        permissions = ClientTokenPermission()
        self.assertTrue(permissions.has_permission(request, None))

    def test_valid_token_in_header__has_permission(self):
        request = self.request_factory.get('/', **self.get_token_headers())
        permissions = ClientTokenPermission()
        self.assertTrue(permissions.has_permission(request, None))

    def test_token_permissions_check_decorates_request(self):
        request = self.request_factory.get('/', **self.get_token_headers())
        permissions = ClientTokenPermission()
        permissions.has_permission(request, None)
        self.assertTrue(request.has_valid_token)
