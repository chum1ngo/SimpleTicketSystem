from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Ticket


class TicketAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )

    def test_rejects_unauthenticated_request(self):
        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, 401)

    def test_accepts_authenticated_request(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, 200)

    def test_rejects_unauthenticated_ticket_detail_request(self):
        ticket = Ticket.objects.create(
            title="Test Ticket",
            description="Test description",
            priority="LOW",
        )

        response = self.client.get(f"/tickets/{ticket.id}/")
        self.assertEqual(response.status_code, 401)


class TokenAuthenticationEndpointTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )

    def test_returns_token_for_valid_credentials(self):
        response = self.client.post(
            "/api-token-auth/",
            {"username": "test_user", "password": "test_password"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api-token-auth/",
            {"username": "test_user", "password": "wrong_password"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("token", response.data)

    def test_validates_token_exists_and_belongs_to_user(self):
        response = self.client.post(
            "/api-token-auth/",
            {"username": "test_user", "password": "test_password"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        token_key = response.data["token"]

        token = Token.objects.get(key=token_key)
        self.assertEqual(token.user, self.user)

    def test_accesses_protected_endpoint_with_token(self):
        response = self.client.post(
            "/api-token-auth/",
            {"username": "test_user", "password": "test_password"},
            format="json",
        )

        token_key = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_key}")

        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, 200)

    def test_rejects_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid_token")

        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, 401)
