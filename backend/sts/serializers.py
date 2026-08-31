from rest_framework import serializers

from .models import Ticket, Comment


class TicketSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = ["created_at", "created_by"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "ticket", "content", "created_at"]
        read_only_fields = ["ticket", "created_at"]
