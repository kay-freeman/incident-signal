from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SupportTicket:
    ticket_id: str
    created_at: datetime
    category: str
    summary: str


@dataclass(frozen=True)
class Incident:
    category: str
    ticket_count: int
    first_seen: datetime
    last_seen: datetime
    ticket_ids: tuple[str, ...]