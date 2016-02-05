import logging

from rest_framework import permissions

from .conf import TOKEN_HEADER
from .models import Token


LOGGER = logging.getLogger('drfutils.permissions')
HTTP_TOKEN_LOOKUP = "HTTP_" + TOKEN_HEADER.replace('-', '_').upper()


def contains_valid_token(request):
    """
    Check that the request contains a registered token.

    The request must include a header or querystring argument
    `TOKEN_HEADER` to match a token for a registered client.

    """
    access_token = request.META.get(HTTP_TOKEN_LOOKUP)

    if access_token is None:
        access_token = request.GET.get(TOKEN_HEADER)

    if access_token is not None:
        token_matched = Token.objects.filter(key=access_token).exists()
        if not token_matched:
            LOGGER.error(
                "Token provided ({0}) "
                "didn't match any existing token".format(access_token)
            )
        return token_matched

    return False


class ClientTokenPermission(permissions.BasePermission):
    """
    A special permissions checker based on tokens.

    """
    def has_permission(self, request, view):
        """
        Will only allow access if token matches that of a registered client.

        A token may be included as a proprietary HTTP header or as part of
        the query string (this is useful when clients cannot set HTTP headers,
        e.g. when testing with a browser).

        This security check is intentionally simplistic for now. Later on we
        may want to match originating host/domain and token.
        """
        request.has_valid_token = contains_valid_token(request)
        return request.has_valid_token

    def has_object_permission(self, request, view, obj):
        """
        Permissions to objects will be granted if token check was successful
        """
        return self.has_permission(request, view)


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Allows access only to authenticated users.

    This is intended as a replacement for built-in IsAuthenticated, that
    returns True on has_object_permission regardless of authenticated user,
    making it unsuitable for use with the AnyPermission logical-OR chaining.

    """
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class AnyPermissions(permissions.BasePermission):
    """
    DRF permission chaining using an 'OR' logic

    In standard DRF, when you specify multiple permissions classes, they all
    have to allow access for the permission to work ('AND'). This class allows
    chaining alternative permission checks (as in logged in users versus
    token-based permission.

    Permissions are set by defining an attribute in the view named
    'any_permission_classes'

    """
    def get_permissions(self, view):
        """
        Get all of the permissions classes that are associated with the view.
        """

        return getattr(view, "any_permission_classes", [])

    def has_permission(self, request, view):
        """
        Check the permissions on the view.
        """

        permissions = self.get_permissions(view)

        for perm_class in permissions:
            permission = perm_class()

            if permission.has_permission(request, view):
                return True

        return not permissions

    def has_object_permission(self, request, view, obj):
        """
        Check the object permissions on the view.
        """

        permissions = self.get_permissions(view)

        for perm_class in permissions:
            permission = perm_class()

            if permission.has_object_permission(request, view, obj):
                return True

        return not permissions
