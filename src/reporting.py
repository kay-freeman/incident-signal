import json
from pathlib import Path

from .models import Incident


def build_text_report(
    input_file: str | Path,
    tickets_analyzed: int,
    incidents: list[Incident],
    threshold: int,
    window_minutes: int,
) -> str:
    lines = [
        f"Input file: {input_file}",
        f"Analyzed {tickets_analyzed} support tickets.",
        (
            f"Detection rule: {threshold} tickets "
            f"within {window_minutes} minutes."
        ),
    ]

    if not incidents:
        lines.append("No potential incidents detected.")
        return "\n".join(lines)

    lines.append(
        f"Detected {len(incidents)} potential incident(s):"
    )

    for incident in incidents:
        ticket_ids = ", ".join(incident.ticket_ids)

        lines.extend(
            [
                "",
                f"Category: {incident.category}",
                f"Severity: {incident.severity}",
                f"Ticket count: {incident.ticket_count}",
                f"First seen: {incident.first_seen}",
                f"Last seen: {incident.last_seen}",
                f"Tickets: {ticket_ids}",
            ]
        )

    return "\n".join(lines)


def build_json_report(
    input_file: str | Path,
    tickets_analyzed: int,
    incidents: list[Incident],
    threshold: int,
    window_minutes: int,
) -> str:
    report = {
        "input_file": str(input_file),
        "summary": {
            "tickets_analyzed": tickets_analyzed,
            "incidents_detected": len(incidents),
        },
        "detection_rule": {
            "threshold": threshold,
            "window_minutes": window_minutes,
        },
        "incidents": [
            {
                "category": incident.category,
                "severity": incident.severity,
                "ticket_count": incident.ticket_count,
                "first_seen": incident.first_seen.isoformat(),
                "last_seen": incident.last_seen.isoformat(),
                "ticket_ids": list(incident.ticket_ids),
            }
            for incident in incidents
        ],
    }

    return json.dumps(report, indent=2)


def save_report(
    report_content: str,
    output_file: str | Path,
) -> Path:
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_content, encoding="utf-8")

    return output_path