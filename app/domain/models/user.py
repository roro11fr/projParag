from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    company_id: int
    username: str
    email: str
    role: str
    created_at: Optional[datetime] = None