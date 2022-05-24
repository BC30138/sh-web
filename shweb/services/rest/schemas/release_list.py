from marshmallow import Schema, fields, pre_load, post_dump, validate
# from shweb.services.rest.translate_helpers import get_release_types


class ReleaseListItemSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(["single", "album", "ep"]))

    @pre_load
    def pre_load_func(self, in_data, **kwargs):
        if 'type' in in_data:
            in_data['type'] = in_data['type'].lower()
        return in_data

    # @post_dump
    # def post_dump_function(self, data, **kwargs):
    #     data['lang_type'] = get_release_types()[data['type']] compile_release_type(_, True)
    #     return data


class ReleaseListSchema(Schema):
    releases = fields.List(fields.Nested(ReleaseListItemSchema), required=True)

    @post_dump
    def post_dump_function(self, data, **kwargs):
        return data['releases']
