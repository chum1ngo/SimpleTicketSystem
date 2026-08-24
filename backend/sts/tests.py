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

