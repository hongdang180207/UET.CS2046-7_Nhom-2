from dataclasses import dataclass
from typing import Literal


CategoryType = Literal["income", "expense"]


@dataclass
class Category:
    category_id: int
    name: str
    category_type: CategoryType
    is_active: bool