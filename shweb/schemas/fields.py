from marshmallow import fields, exceptions
from shweb.utils import get_release_types, get_month_name


class DateString(fields.Str):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        date_month = value.split()[1]
        return value.replace(date_month, get_month_name()[date_month])


class ReleaseType(fields.Str):
    allowed = ["Single", "Album", "EP"]

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if value not in self.allowed:
            raise exceptions.ValidationError(f"Field should be one of: {self.allowed}")
        return get_release_types()[value]
