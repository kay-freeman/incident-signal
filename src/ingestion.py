import json
from datetime import datetime
from pathlib import Path

from .models import SupportTicket


REQUIRED_FIELDS = {"ticket_id", "created_at", "category", "summary"}


def require_non_empty_string(
    item: dict,
    field_name: str,
    position: int,
) -> str:
    value = item[field_name]

    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Ticket at position {position} has an invalid "
            f"'{field_name}' value."
        )

    return value.strip()


def load_tickets(file_path: str | Path) -> list[SupportTicket]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        ticket_data = json.load(file)

    if not isinstance(ticket_data, list):
        raise ValueError("Ticket data must be a list.")

    tickets = []
    seen_ticket_ids = set()

    for position, item in enumerate(ticket_data, start=1):
        if not isinstance(item, dict):
            raise ValueError(
                f"Ticket at position {position} must be an object."
            )

        missing_fields = REQUIRED_FIELDS - item.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Ticket at position {position} is missing: {missing}"
            )

        ticket_id = require_non_empty_string(
            item, "ticket_id", position
        )
        created_at_value = require_non_empty_string(
            item, "created_at", position
        )
        category = require_non_empty_string(
            item, "category", position
        )
        summary = require_non_empty_string(
            item, "summary", position
        )

        if ticket_id in seen_ticket_ids:
            raise ValueError(
                f"Duplicate ticket_id at position {position}: {ticket_id}"
            )

        try:
            created_at = datetime.fromisoformat(created_at_value)
        except ValueError:
            raise ValueError(
                f"Ticket '{ticket_id}' has an invalid "
                f"'created_at' timestamp: {created_at_value}"
            )

        seen_ticket_ids.add(ticket_id)

        tickets.append(
            SupportTicket(
                ticket_id=ticket_id,
                created_at=created_at,
                category=category,
                summary=summary,
            )
        )

    return sorted(tickets, key=lambda ticket: ticket.created_at)