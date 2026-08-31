from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from ..models import Ticket


class TicketCommentViewTests(APITestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            title="Ticket with comments",
            description="Ticket used to test comments",
            priority="MEDIUM",
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)

    def test_creates_comment_for_ticket(self):
        response = self.client.post(
            f"/tickets/{self.ticket.id}/comments/",
            {"content": "First comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["content"], "First comment")
        self.assertEqual(self.ticket.comments.count(), 1)
        self.assertEqual(self.ticket.comments.get().content, "First comment")

    def test_rejects_comment_without_content(self):
        response = self.client.post(
            f"/tickets/{self.ticket.id}/comments/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("content", response.data)
        self.assertEqual(self.ticket.comments.count(), 0)

    def test_rejects_comment_with_empty_content(self):
        response = self.client.post(
            f"/tickets/{self.ticket.id}/comments/",
            {"content": ""},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("content", response.data)
        self.assertEqual(self.ticket.comments.count(), 0)

    def test_returns_404_when_comment_ticket_does_not_exist(self):
        response = self.client.post(
            "/tickets/999/comments/",
            {"content": "Orphan comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_rejects_unauthenticated_comment_list_request(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(f"/tickets/{self.ticket.id}/comments/")

        self.assertEqual(response.status_code, 401)

    def test_rejects_unauthenticated_comment_creation_request(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            f"/tickets/{self.ticket.id}/comments/",
            {"content": "First comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_returns_empty_comment_list(self):
        response = self.client.get(f"/tickets/{self.ticket.id}/comments/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_lists_only_comments_from_requested_ticket(self):
        other_ticket = Ticket.objects.create(
            title="Other ticket",
            description="Ticket whose comments must not be returned",
            priority="LOW",
        )

        first_response = self.client.post(
            f"/tickets/{self.ticket.id}/comments/",
            {"content": "Expected comment"},
            format="json",
        )
        second_response = self.client.post(
            f"/tickets/{other_ticket.id}/comments/",
            {"content": "Comment from another ticket"},
            format="json",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)

        response = self.client.get(f"/tickets/{self.ticket.id}/comments/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], "Expected comment")

    def test_assigns_authenticated_user_as_comment_creator(self):
        response = self.client.post(
            f"/tickets/{self.ticket.id}/comments/",
            {"content": "Comment with creator"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        comment = self.ticket.comments.get()
        self.assertEqual(comment.created_by, self.user)

    def test_assigns_developer_comment_type_from_user_group(self):
        developer_group = Group.objects.create(name="Developer")
        self.user.groups.add(developer_group)

        response = self.client.post(
            f"/tickets/{self.ticket.id}/comments/",
            {"content": "Developer comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        comment = self.ticket.comments.get()
        self.assertEqual(comment.comment_type, "DEVELOPER")
