from rest_framework import serializers

from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "ticket",
            "content",
            "created_at",
            "created_by",
            "comment_type",
        ]
        read_only_fields = [
            "ticket",
            "created_at",
            "created_by",
            "comment_type",
        ]
