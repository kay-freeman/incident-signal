import argparse
import json
from pathlib import Path

from .detection import detect_incidents
from .ingestion import load_tickets


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TICKET_FILE = PROJECT_ROOT / "data" / "sample_tickets.json"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect incident patterns across support tickets."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_TICKET_FILE,
        help="Path to a JSON ticket file.",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Minimum number of related tickets required (default: 3).",
    )

    parser.add_argument(
        "--window",
        type=int,
        default=30,
        help="Detection window in minutes (default: 30).",
    )

    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()

    try:
        tickets = load_tickets(arguments.input)
        incidents = detect_incidents(
            tickets,
            threshold=arguments.threshold,
            window_minutes=arguments.window,
        )
    except FileNotFoundError:
        raise SystemExit(
            f"Error: Input file not found: {arguments.input}"
        )
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"Error: Invalid JSON in {arguments.input} "
            f"at line {error.lineno}, column {error.colno}."
        )
    except ValueError as error:
        raise SystemExit(f"Error: {error}")

    print(f"Input file: {arguments.input}")
    print(f"Analyzed {len(tickets)} support tickets.")
    print(
        f"Detection rule: {arguments.threshold} tickets "
        f"within {arguments.window} minutes."
    )

    if not incidents:
        print("No potential incidents detected.")
        return

    print(f"Detected {len(incidents)} potential incident(s):")

    for incident in incidents:
        ticket_ids = ", ".join(incident.ticket_ids)

        print()
        print(f"Category: {incident.category}")
        print(f"Ticket count: {incident.ticket_count}")
        print(f"First seen: {incident.first_seen}")
        print(f"Last seen: {incident.last_seen}")
        print(f"Tickets: {ticket_ids}")


if __name__ == "__main__":
    main()