from collections import defaultdict
from datetime import timedelta

from .models import Incident, SupportTicket


def split_activity_clusters(
    tickets: list[SupportTicket],
    allowed_window: timedelta,
) -> list[list[SupportTicket]]:
    clusters = []
    current_cluster = []

    for ticket in tickets:
        if (
            current_cluster
            and ticket.created_at - current_cluster[-1].created_at
            > allowed_window
        ):
            clusters.append(current_cluster)
            current_cluster = []

        current_cluster.append(ticket)

    if current_cluster:
        clusters.append(current_cluster)

    return clusters


def contains_qualifying_window(
    tickets: list[SupportTicket],
    threshold: int,
    allowed_window: timedelta,
) -> bool:
    window_start = 0

    for window_end, ticket in enumerate(tickets):
        while (
            ticket.created_at - tickets[window_start].created_at
            > allowed_window
        ):
            window_start += 1

        tickets_in_window = window_end - window_start + 1

        if tickets_in_window >= threshold:
            return True

    return False


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

        activity_clusters = split_activity_clusters(
            category_tickets,
            allowed_window,
        )

        for cluster in activity_clusters:
            if not contains_qualifying_window(
                cluster,
                threshold,
                allowed_window,
            ):
                continue

            incidents.append(
                Incident(
                    category=category,
                    ticket_count=len(cluster),
                    first_seen=cluster[0].created_at,
                    last_seen=cluster[-1].created_at,
                    ticket_ids=tuple(
                        ticket.ticket_id for ticket in cluster
                    ),
                )
            )

    return sorted(incidents, key=lambda incident: incident.first_seen)