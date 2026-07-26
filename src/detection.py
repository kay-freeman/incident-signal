from collections import defaultdict
from datetime import timedelta

from .models import Incident, SupportTicket


def detect_incidents(
    tickets: list[SupportTicket],
    threshold: int = 3,
    window_minutes: int = 30,
) -> list[Incident]:
    if threshold < 1:
        raise ValueError("Threshold must be at least 1.")

    if window_minutes < 1:
        raise ValueError("Window must be at least 1 minute.")

    tickets_by_category = defaultdict(list)

    for ticket in tickets:
        tickets_by_category[ticket.category].append(ticket)

    incidents = []
    allowed_window = timedelta(minutes=window_minutes)

    for category, category_tickets in tickets_by_category.items():
        category_tickets.sort(key=lambda ticket: ticket.created_at)

        window_start = 0
        largest_cluster = []

        for window_end, ticket in enumerate(category_tickets):
            while (
                ticket.created_at
                - category_tickets[window_start].created_at
                > allowed_window
            ):
                window_start += 1

            current_cluster = category_tickets[window_start : window_end + 1]

            if len(current_cluster) > len(largest_cluster):
                largest_cluster = current_cluster

        if len(largest_cluster) >= threshold:
            incidents.append(
                Incident(
                    category=category,
                    ticket_count=len(largest_cluster),
                    first_seen=largest_cluster[0].created_at,
                    last_seen=largest_cluster[-1].created_at,
                    ticket_ids=tuple(
                        ticket.ticket_id for ticket in largest_cluster
                    ),
                )
            )

    return sorted(incidents, key=lambda incident: incident.first_seen)