import json
from datetime import datetime
from pathlib import Path

from src.models import Incident
from src.reporting import (
    build_json_report,
    build_text_report,
    save_report,
)


def sample_incident() -> Incident:
    return Incident(
        category="login_failure",
        severity="medium",
        ticket_count=3,
        first_seen=datetime.fromisoformat("2026-07-26T09:00:00"),
        last_seen=datetime.fromisoformat("2026-07-26T09:20:00"),
        ticket_ids=("TKT-1", "TKT-2", "TKT-3"),
    )


def test_builds_readable_text_report() -> None:
    report = build_text_report(
        input_file="data/sample_tickets.json",
        tickets_analyzed=3,
        incidents=[sample_incident()],
        threshold=3,
        window_minutes=30,
    )

    assert "Analyzed 3 support tickets." in report
    assert "Detected 1 potential incident(s):" in report
    assert "Category: login_failure" in report
    assert "Severity: medium" in report
    assert "Tickets: TKT-1, TKT-2, TKT-3" in report


def test_builds_structured_json_report() -> None:
    report_json = build_json_report(
        input_file="data/sample_tickets.json",
        tickets_analyzed=3,
        incidents=[sample_incident()],
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
    assert report["incidents"][0]["severity"] == "medium"
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


def test_saves_report_and_creates_parent_directory(
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "reports" / "incident-report.json"
    report_content = '{"status": "complete"}'

    saved_path = save_report(report_content, output_file)

    assert saved_path == output_file
    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == report_content