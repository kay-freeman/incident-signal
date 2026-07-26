import json
from datetime import datetime
from pathlib import Path

from .models import SupportTicket


REQUIRED_FIELDS = {"ticket_id", "created_at", "category", "summary"}


def load_tickets(file_path: str | Path) -> list[SupportTicket]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        ticket_data = json.load(file)

    if not isinstance(ticket_data, list):
        raise ValueError("Ticket data must be a list.")

    tickets = []

    for position, item in enumerate(ticket_data, start=1):
        missing_fields = REQUIRED_FIELDS - item.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Ticket at position {position} is missing: {missing}"
            )

        ticket = SupportTicket(
            ticket_id=item["ticket_id"],
            created_at=datetime.fromisoformat(item["created_at"]),
            category=item["category"],
            summary=item["summary"],
        )
        tickets.append(ticket)

    return sorted(tickets, key=lambda ticket: ticket.created_at)