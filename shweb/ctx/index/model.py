"""Представление для данных индекс-страницы"""

import dataclasses
from typing import Optional, List


@dataclasses.dataclass
class ClientIndexEntity:
    style: str
    content: str

    def to_dict(self):
        return {
            'style': self.style,
            'content': self.content,
        }


@dataclasses.dataclass
class IndexEntity:
    web: ClientIndexEntity
    mobile: ClientIndexEntity
    files_list: Optional[List[str]]

    def to_dict(self):
        return {
            'web': self.web.to_dict(),
            'mobile': self.mobile.to_dict(),
            'files_list': [] if not self.files_list else self.files_list,
        }
