from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from ..models import Ticket


class TicketAssignmentTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()

        self.developer = user_model.objects.create_user(
            username="developer",
            password="test_password",
        )
        self.developer.groups.add(Group.objects.get(name="Developer"))

        self.qa = user_model.objects.create_user(
            username="qa",
            password="test_password",
        )
        self.qa.groups.add(Group.objects.get(name="QA"))

        self.requester = user_model.objects.create_user(
            username="requester",
            password="test_password",
        )
        self.requester.groups.add(Group.objects.get(name="Requester"))

        self.ticket = Ticket.objects.create(
            title="Assignment test ticket",
            description="Ticket used to test assignment",
            created_by=self.requester,
        )
        self.client.force_authenticate(user=self.developer)

    def test_developer_assigns_ticket_to_qa(self):
        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"assigned_to": self.qa.id},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.qa)
        self.assertEqual(self.ticket.ticket_status, "ASIGNADA")

    def test_qa_assigns_ticket_to_developer(self):
        self.client.force_authenticate(user=self.qa)

        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"assigned_to": self.developer.id},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.developer)

    def test_developer_assigns_ticket_to_self(self):
        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"assigned_to": self.developer.id},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.developer)

    def test_rejects_assignment_to_requester(self):
        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"assigned_to": self.requester.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("assigned_to", response.data)
        self.ticket.refresh_from_db()
        self.assertIsNone(self.ticket.assigned_to)

    def test_requester_cannot_assign_ticket(self):
        self.client.force_authenticate(user=self.requester)

        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"assigned_to": self.developer.id},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.ticket.refresh_from_db()
        self.assertIsNone(self.ticket.assigned_to)

    def test_unassigning_ticket_changes_status_to_unassigned(self):
        self.ticket.assigned_to = self.developer
        self.ticket.ticket_status = Ticket.TicketStatus.ASIGNADA
        self.ticket.save()

        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"assigned_to": None},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertIsNone(self.ticket.assigned_to)
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

    def test_reassigns_ticket(self):
        self.ticket.assigned_to = self.developer
        self.ticket.ticket_status = Ticket.TicketStatus.ASIGNADA
        self.ticket.save()

        self.client.force_authenticate(user=self.qa)
        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"assigned_to": self.qa.id},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.qa)
        self.assertEqual(self.ticket.ticket_status, "ASIGNADA")

    def test_assignment_overrides_conflicting_unassigned_status(self):
        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {
                "assigned_to": self.qa.id,
                "ticket_status": "SIN_ASIGNAR",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.qa)
        self.assertEqual(self.ticket.ticket_status, "ASIGNADA")
