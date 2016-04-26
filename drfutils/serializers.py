def get_querystring_fields(serializer, arg_name):
    """
    Gets a list of fields from the querystring that exist in the serializer

    """
    if 'request' in serializer.context:
        fields = serializer.context['request'].query_params.get(arg_name, None)

        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(serializer.fields.keys())
            return allowed & existing
    return None


class FieldLimiterMixin(object):
    def keep_only_fields(self, fields):
        if fields is not None:
            existing = set(self.fields.keys())
            for field_name in existing - fields:
                self.fields.pop(field_name)


class DynamicFieldsSerializerMixin(FieldLimiterMixin):
    """
    Limit the number of fields to be retrieved as per request querystring.

    A ModelSerializer mixin that accepts a `fields` within its views GET params
    controlling which fields should be displayed. this should be mixed into the
    serializer on which you want this ability.

    Example: ``/blips/?fields=id,content``

    """
    def __init__(self, *args, **kwargs):
        """
        Change the subset of fields to display based on request query params.

        Look at the context, see if we have been passed through `fields`,
        if we have, drop any fields that are not specified

        """
        super().__init__(*args, **kwargs)
        fields = get_querystring_fields(self, 'fields')
        self.keep_only_fields(fields)


class LimitedFieldsSerializerMixin(FieldLimiterMixin):
    """
    Limit the number of fields to be retrieved to Meta.only_fields

    """
    def __init__(self, *args, **kwargs):
        """
        Change the subset of fields to display based on only_fields

        """
        super().__init__(*args, **kwargs)
        fields = set(self.Meta.only_fields)
        self.keep_only_fields(fields)


class ExpandableFieldsSerializerMixin(object):
    """
    Expand fields optionally to use serializers

    A ModelSerializer mixin that accepts `expand` as a query string argument
    controlling which fields should be expanded.

    The expansion means that certain fields that are by default rendered
    using a URL will render a serialized object instead. The serializer to
    use for the embedded object will be determined from a `Meta` option
    `expansions`.

    Example: ``/blips/?expand=parent``

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        expand = get_querystring_fields(self, 'expand')

        if expand is not None:
            for field_name in expand:
                serializer_class = self.Meta.expansions.get(field_name, None)
                if serializer_class:
                    self.fields[field_name] = serializer_class(
                        context=self.context
                    )


def SubSerializer(original_serializer_class, fields):
    new_meta = type(
        'Meta',
        (original_serializer_class.Meta,),
        {'only_fields': fields}
    )
    serializer_class = type(
        'Sub{}'.format(original_serializer_class.__name__),
        (LimitedFieldsSerializerMixin, original_serializer_class),
        {'Meta': new_meta}
    )
    return serializer_class
