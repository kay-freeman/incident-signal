import json
from pathlib import Path

from .models import Incident


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
                "ticket_count": incident.ticket_count,
                "first_seen": incident.first_seen.isoformat(),
                "last_seen": incident.last_seen.isoformat(),
                "ticket_ids": list(incident.ticket_ids),
            }
            for incident in incidents
        ],
    }

    return json.dumps(report, indent=2)