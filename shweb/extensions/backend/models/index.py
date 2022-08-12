from dataclasses import field
from marshmallow_dataclass import dataclass
from marshmallow_enum import EnumField

from shweb.app.helpers.enums import LangEnum

@dataclass
class IndexQueryArgs:  
    is_mobile: bool = field(default=False)
    language: LangEnum = field(
        default=LangEnum.en,
        metadata=dict(
            marshmallow_field=EnumField(
                LangEnum,
                by_value=True,
                allow_none=True,
            ),
        ),
    )

