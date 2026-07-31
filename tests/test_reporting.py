import json
from datetime import datetime

from src.models import Incident
from src.reporting import build_json_report


def test_builds_structured_json_report() -> None:
    incident = Incident(
        category="login_failure",
        ticket_count=3,
        first_seen=datetime.fromisoformat("2026-07-26T09:00:00"),
        last_seen=datetime.fromisoformat("2026-07-26T09:20:00"),
        ticket_ids=("TKT-1", "TKT-2", "TKT-3"),
    )

    report_json = build_json_report(
        input_file="data/sample_tickets.json",
        tickets_analyzed=3,
        incidents=[incident],
        threshold=3,
        window_minutes=30,
    )

    report = json.loads(report_json)

    assert report["input_file"] == "data/sample_tickets.json"
    assert report["summary"]["tickets_analyzed"] == 3
    assert report["summary"]["incidents_detected"] == 1
    assert report["detection_rule"]["threshold"] == 3
    assert report["detection_rule"]["window_minutes"] == 30
    assert report["incidents"][0]["category"] == "login_failure"
    assert report["incidents"][0]["ticket_count"] == 3
    assert report["incidents"][0]["first_seen"] == "2026-07-26T09:00:00"
    assert report["incidents"][0]["last_seen"] == "2026-07-26T09:20:00"
    assert report["incidents"][0]["ticket_ids"] == [
        "TKT-1",
        "TKT-2",
        "TKT-3",
    ]


def test_builds_report_with_no_incidents() -> None:
    report_json = build_json_report(
        input_file="data/sample_tickets.json",
        tickets_analyzed=2,
        incidents=[],
        threshold=3,
        window_minutes=30,
    )

    report = json.loads(report_json)

    assert report["summary"]["tickets_analyzed"] == 2
    assert report["summary"]["incidents_detected"] == 0
    assert report["incidents"] == []