"""Представление для данных индекс-страницы"""

import dataclasses
from typing import Optional, List


@dataclasses.dataclass
class ClientIndexEntity:
    style: str
    content: str


@dataclasses.dataclass
class IndexEntity:
    web: ClientIndexEntity
    mobile: ClientIndexEntity
    files_list: Optional[List[str]]
