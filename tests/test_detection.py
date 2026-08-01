from datetime import datetime

import pytest

from src.detection import detect_incidents
from src.models import SupportTicket


def make_ticket(
    ticket_id: str,
    created_at: str,
    category: str = "login_failure",
) -> SupportTicket:
    return SupportTicket(
        ticket_id=ticket_id,
        created_at=datetime.fromisoformat(created_at),
        category=category,
        summary="Synthetic test ticket",
    )


def test_detects_ticket_cluster() -> None:
    tickets = [
        make_ticket("TKT-1", "2026-07-26T09:00:00"),
        make_ticket("TKT-2", "2026-07-26T09:10:00"),
        make_ticket("TKT-3", "2026-07-26T09:20:00"),
    ]

    incidents = detect_incidents(tickets)

    assert len(incidents) == 1
    assert incidents[0].category == "login_failure"
    assert incidents[0].ticket_count == 3


def test_ignores_categories_below_threshold() -> None:
    tickets = [
        make_ticket("TKT-1", "2026-07-26T09:00:00"),
        make_ticket("TKT-2", "2026-07-26T09:10:00"),
    ]

    incidents = detect_incidents(tickets)

    assert incidents == []


def test_ignores_tickets_outside_time_window() -> None:
    tickets = [
        make_ticket("TKT-1", "2026-07-26T09:00:00"),
        make_ticket("TKT-2", "2026-07-26T09:31:00"),
        make_ticket("TKT-3", "2026-07-26T10:02:00"),
    ]

    incidents = detect_incidents(tickets)

    assert incidents == []


def test_rejects_invalid_threshold() -> None:
    with pytest.raises(ValueError, match="Threshold must be at least 1"):
        detect_incidents([], threshold=0)


def test_detects_multiple_incidents_in_same_category() -> None:
    tickets = [
        make_ticket("TKT-1", "2026-07-26T09:00:00"),
        make_ticket("TKT-2", "2026-07-26T09:10:00"),
        make_ticket("TKT-3", "2026-07-26T09:20:00"),
        make_ticket("TKT-4", "2026-07-26T16:00:00"),
        make_ticket("TKT-5", "2026-07-26T16:10:00"),
        make_ticket("TKT-6", "2026-07-26T16:20:00"),
    ]

    incidents = detect_incidents(tickets)

    assert len(incidents) == 2
    assert incidents[0].ticket_ids == ("TKT-1", "TKT-2", "TKT-3")
    assert incidents[1].ticket_ids == ("TKT-4", "TKT-5", "TKT-6")


def test_activity_cluster_still_requires_qualifying_window() -> None:
    tickets = [
        make_ticket("TKT-1", "2026-07-26T09:00:00"),
        make_ticket("TKT-2", "2026-07-26T09:25:00"),
        make_ticket("TKT-3", "2026-07-26T09:50:00"),
    ]

    incidents = detect_incidents(tickets)

    assert incidents == []