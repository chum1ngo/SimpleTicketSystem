from rest_framework.test import APITestCase
from .models import Ticket

class TicketListViewTests(APITestCase):
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


class TicketDetailsViewTests(APITestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            title="Test Ticket",
            description="Test description",
            priority="LOW",
        )

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
            priority="LOW"
        )

    def test_returns_ticket_initial_status(self):
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

    def test_changes_ticket_status(self):
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

        response = self.client.patch(f"/tickets/{self.ticket.id}/", {"ticket_status": "ASIGNADA"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status, "ASIGNADA")

    def test_returns_400_error_for_invalid_status(self):
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

        response = self.client.patch(f"/tickets/{self.ticket.id}/", {"ticket_status": "INVALID"}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("ticket_status", response.data)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status, "SIN_ASIGNAR")

    def test_returns_404_for_nonexistent_ticket(self):
        response = self.client.patch("/tickets/999/", {"ticket_status": "ASIGNADA"}, format="json")

        self.assertEqual(response.status_code, 404)
