from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Ticket


class TicketListViewTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)

    def test_returns_existing_tickets(self):
        Ticket.objects.create(
            title="Test Ticket",
            description="Test description",
            priority="LOW",
        )

        response = self.client.get("/tickets/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Ticket")


class CreateTicketViewTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)

    def test_creates_new_ticket(self):
        response = self.client.post(
            "/tickets/",
            {
                "title": "New Ticket",
                "description": "New description",
                "priority": "HIGH",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ticket.objects.count(), 1)

        ticket = Ticket.objects.get()
        self.assertEqual(ticket.title, "New Ticket")
        self.assertEqual(ticket.description, "New description")
        self.assertEqual(ticket.priority, "HIGH")

    def test_rejects_ticket_without_title(self):
        response = self.client.post(
            "/tickets/",
            {
                "description": "New description",
                "priority": "HIGH",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ticket.objects.count(), 0)
        self.assertIn("title", response.data)

    def test_uses_medium_priority_when_priority_is_not_provided(self):
        response = self.client.post(
            "/tickets/",
            {
                "title": "New Ticket",
                "description": "New description",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ticket.objects.count(), 1)

        ticket = Ticket.objects.get()
        self.assertEqual(ticket.title, "New Ticket")
        self.assertEqual(ticket.description, "New description")
        self.assertEqual(ticket.priority, "MEDIUM")

    def test_rejects_ticket_with_invalid_priority(self):
        response = self.client.post(
            "/tickets/",
            {
                "title": "New Ticket",
                "description": "New description",
                "priority": "URGENT",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ticket.objects.count(), 0)
        self.assertIn("priority", response.data)
