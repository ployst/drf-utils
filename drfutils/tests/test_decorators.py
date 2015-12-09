from unittest import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from ..decorators import auto404


@auto404
def i_may_fail(exception=None):
    if exception:
        raise exception
    else:
        return 'Weee'


class SomeWeirdException(Exception):
    pass


class TestAuto404(TestCase):
    def test_raises_http404_on_object_not_found(self):
        with self.assertRaises(Http404):
            i_may_fail(ObjectDoesNotExist())

    def test_proceeds_normally_on_no_exception(self):
        result = i_may_fail()

        self.assertEqual(result, 'Weee')

    def test_passes_along_other_exceptions(self):
        with self.assertRaises(SomeWeirdException):
            i_may_fail(SomeWeirdException())
