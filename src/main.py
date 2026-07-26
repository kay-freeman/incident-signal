import argparse
from pathlib import Path

from .detection import detect_incidents
from .ingestion import load_tickets


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TICKET_FILE = PROJECT_ROOT / "data" / "sample_tickets.json"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect incident patterns across support tickets."
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
    tickets = load_tickets(TICKET_FILE)

    incidents = detect_incidents(
        tickets,
        threshold=arguments.threshold,
        window_minutes=arguments.window,
    )

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