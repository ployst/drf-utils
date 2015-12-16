from hashlib import md5

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField


class GravatarField(serializers.Field):
    def to_representation(self, obj):
        return '//gravatar.com/avatar/{}'.format(
            md5(obj.lower().encode('utf-8')).hexdigest()
        )


class MixedRelatedField(PrimaryKeyRelatedField):
    """
    A relation field that behaves as PK for write and URL for read.

    """
    def __init__(self, render_with, queryset=None):
        super().__init__(queryset=queryset)
        self.render_with = render_with

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        self.render_with.bind(field_name, parent)

    def to_representation(self, value):
        return self.render_with.to_representation(value)
