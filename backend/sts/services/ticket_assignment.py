from ..models import Ticket
from ..roles import UserRole, get_user_role


class InvalidAssigneeError(ValueError):
    pass


def validate_assignee(user):
    if user is None:
        return

    if get_user_role(user) not in {UserRole.DEVELOPER, UserRole.QA}:
        raise InvalidAssigneeError(
            "Tickets can only be assigned to Developer or QA users."
        )


def update_ticket(*, ticket, changes):
    changes = dict(changes)

    if "assigned_to" in changes:
        assigned_to = changes["assigned_to"]
        validate_assignee(assigned_to)
        changes["ticket_status"] = (
            Ticket.TicketStatus.ASIGNADA
            if assigned_to is not None
            else Ticket.TicketStatus.SIN_ASIGNAR
        )

    for field, value in changes.items():
        setattr(ticket, field, value)

    ticket.save()
    return ticket
