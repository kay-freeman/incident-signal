from pathlib import Path

from .detection import detect_incidents
from .ingestion import load_tickets


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TICKET_FILE = PROJECT_ROOT / "data" / "sample_tickets.json"


def main() -> None:
    tickets = load_tickets(TICKET_FILE)
    incidents = detect_incidents(tickets)

    print(f"Analyzed {len(tickets)} support tickets.")

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