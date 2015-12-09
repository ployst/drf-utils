from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def auto404(fun):
    """
    Decorator to generate a 404 response automatically upon DoesNotExist.

    Unfortunately, DRF doesn't do this for you automatically.
    """
    @wraps(fun)
    def _wrapped(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404
    return _wrapped
