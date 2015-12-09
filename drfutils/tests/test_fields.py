from unittest import TestCase

from unittest.mock import Mock
from rest_framework.serializers import Serializer

from ..fields import GravatarField, MixedRelatedField


class TestGravatarField(TestCase):

    def test_gravatar_field(self):
        class SerializerWithGravatar(Serializer):
            gravatar = GravatarField(source='email')

        class ThingWithEmail(object):
            email = 'jim@ployst.com'

        jim = ThingWithEmail()
        serializer = SerializerWithGravatar(jim)

        self.assertEqual(
            serializer.data['gravatar'],
            'http://gravatar.com/avatar/1c3ed1dc72e643886e597e2d07700b3c'
        )


class TestMixedRelatedField(TestCase):

    def test_render_with_another_field(self):
        mock_field = Mock()
        mock_field.to_representation.return_value = 'Woosh'
        mock_queryset = Mock()
        mock_relation = Mock()

        class SerializerWithMixedRelatedField(Serializer):
            related = MixedRelatedField(
                render_with=mock_field,
                queryset=mock_queryset,
            )

        class ThingWithRelation(object):
            related = mock_relation

        thing = ThingWithRelation()
        # serializer = SerializerWithMixedRelatedField(data={'related_id': 24})
        serializer = SerializerWithMixedRelatedField(thing)

        serialized = serializer.data['related']
        self.assertEqual(serialized, 'Woosh')
