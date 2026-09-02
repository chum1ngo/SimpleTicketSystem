from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import TestCase

from ..roles import UserRole, get_user_role


class UserRoleTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_role_user",
            password="test_password",
        )

    def test_role_groups_exist(self):
        group_names = set(
            Group.objects.filter(
                name__in={"Developer", "QA", "Requester"}
            ).values_list("name", flat=True)
        )

        self.assertEqual(group_names, {"Developer", "QA", "Requester"})

    def test_user_without_group_defaults_to_requester(self):
        self.assertEqual(get_user_role(self.user), UserRole.REQUESTER)

    def test_user_cannot_belong_to_multiple_groups(self):
        self.user.groups.add(Group.objects.get(name="Developer"))

        with self.assertRaisesMessage(
            ValidationError,
            "A user can only belong to one group.",
        ):
            with transaction.atomic():
                self.user.groups.add(Group.objects.get(name="QA"))

        self.assertEqual(self.user.groups.count(), 1)

    def test_user_cannot_receive_second_group_from_group_side(self):
        self.user.groups.add(Group.objects.get(name="Developer"))

        with self.assertRaisesMessage(
            ValidationError,
            "A user can only belong to one group.",
        ):
            with transaction.atomic():
                Group.objects.get(name="QA").user_set.add(self.user)

        self.assertEqual(self.user.groups.count(), 1)
