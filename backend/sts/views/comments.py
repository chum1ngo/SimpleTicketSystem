from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Ticket
from ..serializers import CommentSerializer


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticket_comments_read_create(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)

    if request.method == "GET":
        comments = ticket.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
