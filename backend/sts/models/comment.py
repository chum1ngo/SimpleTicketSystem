from django.conf import settings
from django.db import models

from ..roles import UserRole
from .ticket import Ticket


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True,
    )
    comment_type = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        null=True,
        blank=True,
    )
