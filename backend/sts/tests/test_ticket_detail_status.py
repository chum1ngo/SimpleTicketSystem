from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Ticket


class TicketDetailsViewTests(APITestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            title="Test Ticket",
            description="Test description",
            priority="LOW",
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)

    def test_returns_ticket_details(self):
        response = self.client.get(f"/tickets/{self.ticket.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.ticket.id)
        self.assertEqual(response.data["title"], "Test Ticket")
        self.assertEqual(response.data["description"], "Test description")
        self.assertEqual(response.data["priority"], "LOW")

    def test_returns_404_for_nonexistent_ticket(self):
        response = self.client.get("/tickets/999/")

        self.assertEqual(response.status_code, 404)


class TicketStatusViewTests(APITestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            title="Test Ticket",
            description="Test description",
            priority="LOW",
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)

    def test_returns_ticket_initial_status(self):
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

    def test_changes_ticket_status(self):
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"ticket_status": "ASIGNADA"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status, "ASIGNADA")

    def test_returns_400_error_for_invalid_status(self):
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

        response = self.client.patch(
            f"/tickets/{self.ticket.id}/",
            {"ticket_status": "INVALID"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("ticket_status", response.data)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

    def test_returns_404_for_nonexistent_ticket(self):
        response = self.client.patch(
            "/tickets/999/",
            {"ticket_status": "ASIGNADA"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)
