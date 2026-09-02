from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(
        source="assigned_to.username",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "ticket_status",
            "created_at",
            "created_by",
            "assigned_to",
            "assigned_to_username",
        ]
        read_only_fields = [
            "created_at",
            "created_by",
            "assigned_to",
            "assigned_to_username",
        ]


class TicketUpdateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
            "ticket_status",
            "assigned_to",
        ]
