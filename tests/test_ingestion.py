import json
from pathlib import Path

import pytest

from src.ingestion import load_tickets


def valid_ticket() -> dict:
    return {
        "ticket_id": "TKT-1001",
        "created_at": "2026-07-26T09:02:00",
        "category": "login_failure",
        "summary": "User cannot sign in.",
    }


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def test_loads_valid_ticket_data(tmp_path: Path) -> None:
    ticket_file = tmp_path / "tickets.json"
    write_json(ticket_file, [valid_ticket()])

    tickets = load_tickets(ticket_file)

    assert len(tickets) == 1
    assert tickets[0].ticket_id == "TKT-1001"
    assert tickets[0].category == "login_failure"


def test_rejects_data_that_is_not_a_list(tmp_path: Path) -> None:
    ticket_file = tmp_path / "tickets.json"
    write_json(ticket_file, valid_ticket())

    with pytest.raises(ValueError, match="Ticket data must be a list"):
        load_tickets(ticket_file)


def test_rejects_missing_required_fields(tmp_path: Path) -> None:
    ticket_file = tmp_path / "tickets.json"
    incomplete_ticket = valid_ticket()
    del incomplete_ticket["summary"]
    write_json(ticket_file, [incomplete_ticket])

    with pytest.raises(ValueError, match="missing: summary"):
        load_tickets(ticket_file)


def test_rejects_invalid_timestamp(tmp_path: Path) -> None:
    ticket_file = tmp_path / "tickets.json"
    ticket = valid_ticket()
    ticket["created_at"] = "not-a-timestamp"
    write_json(ticket_file, [ticket])

    with pytest.raises(
        ValueError,
        match="invalid 'created_at' timestamp",
    ):
        load_tickets(ticket_file)


def test_rejects_duplicate_ticket_ids(tmp_path: Path) -> None:
    ticket_file = tmp_path / "tickets.json"
    first_ticket = valid_ticket()
    second_ticket = valid_ticket()
    second_ticket["summary"] = "Another report of the same issue"
    write_json(ticket_file, [first_ticket, second_ticket])

    with pytest.raises(ValueError, match="Duplicate ticket_id"):
        load_tickets(ticket_file)


def test_rejects_malformed_json(tmp_path: Path) -> None:
    ticket_file = tmp_path / "tickets.json"
    ticket_file.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_tickets(ticket_file)


def test_missing_file_raises_error(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_tickets(missing_file)