from unittest import TestCase

from unittest.mock import Mock
from rest_framework import fields, serializers

from ..serializers import (
    DynamicFieldsSerializerMixin,
    ExpandableFieldsSerializerMixin,
    SubSerializer,
)


class CreatorSerializer(serializers.Serializer):
    name = fields.CharField()
    other = serializers.SerializerMethodField()
    nickname = fields.CharField()

    class Meta:
        fields = ('name', 'nickname', 'other')

    def get_other(self, *args):
        return 'field in expansion'


class ExpandingSerializer(
        ExpandableFieldsSerializerMixin, serializers.Serializer):
    creator = fields.CharField()

    class Meta:
        expansions = {'creator': CreatorSerializer}


class TestExpandableFieldsSerializer(TestCase):

    def test_expands_requested_fields(self):

        class ThingWithCreator(object):
            creator = {'name': 'jim@ployst.com', 'nickname': 'jim'}

        request = Mock()
        request.query_params.get.return_value = 'creator'

        jim = ThingWithCreator()
        serializer = ExpandingSerializer(jim, context={'request': request})

        self.assertDictEqual(
            serializer.data['creator'],
            {
                'name': 'jim@ployst.com',
                'nickname': 'jim',
                'other': 'field in expansion'
            }
        )

    def test_does_not_expand_by_default(self):

        class ThingWithCreator(object):
            creator = 'jim@ployst.com'

        request = Mock()
        request.query_params.get.return_value = None

        jim = ThingWithCreator()
        serializer = ExpandingSerializer(jim, context={'request': request})

        self.assertEqual(
            serializer.data['creator'], 'jim@ployst.com'
        )


class DynamicSerializer(DynamicFieldsSerializerMixin, serializers.Serializer):
    name = fields.CharField()
    nickname = fields.CharField()


class Thing(object):
    name = 'James'
    nickname = 'thecat'


class TestDynamicFieldsSerializer(TestCase):

    def test_only_returns_requested_fields(self):
        request = Mock()
        request.query_params.get.return_value = 'nickname'

        jim = Thing()
        serializer = DynamicSerializer(jim, context={'request': request})

        self.assertDictEqual(serializer.data, {'nickname': 'thecat'})

    def test_returns_all_fields_by_default(self):
        request = Mock()
        request.query_params.get.return_value = None

        jim = Thing()
        serializer = DynamicSerializer(jim, context={'request': request})

        self.assertDictEqual(
            serializer.data, {'name': 'James', 'nickname': 'thecat'}
        )

    def test_can_return_multiple_fields(self):
        class Thing(object):
            name = 'Jane'
            nickname = 'thesnake'

        request = Mock()
        request.query_params.get.return_value = 'name,nickname'

        jim = Thing()
        serializer = DynamicSerializer(jim, context={'request': request})

        self.assertDictEqual(
            serializer.data, {'name': 'Jane', 'nickname': 'thesnake'}
        )


class TestSerializerBuilder(TestCase):

    def test_only_returns_requested_fields(self):
        serializer_class = SubSerializer(CreatorSerializer, ('nickname',))
        self.assertDictEqual(serializer_class.name, 'SubCreatorSerializer')

    def test_only_returns_requested_fields(self):
        class Thing(object):
            name = 'Only James'
            nickname = 'catnip'

        jim = Thing()
        serializer_class = SubSerializer(CreatorSerializer, ('nickname',))
        serializer = serializer_class(jim)

        self.assertDictEqual(serializer.data, {'nickname': 'catnip'})
