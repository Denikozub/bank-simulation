from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Clerk:
    id: int
    has_client: Optional[int] = None
    service_ending: Optional[datetime] = None
