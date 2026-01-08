from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Company:
    id: Optional[int]
    name: str
    cui: str
    address: Optional[str] = None
    created_at: Optional[datetime] = None