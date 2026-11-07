from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    user_id: int
    display_name: str
    created_at: datetime