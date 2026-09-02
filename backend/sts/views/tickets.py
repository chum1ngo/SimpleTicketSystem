from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Ticket
from ..permissions import IsDeveloperOrQAOrReadOnly
from ..serializers import TicketSerializer, TicketUpdateSerializer
from ..services import InvalidAssigneeError, update_ticket


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticket_list_create(request):
    if request.method == "POST":
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    if request.method == "GET":
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


@api_view(["GET", "PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsDeveloperOrQAOrReadOnly])
def ticket_details_update(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)

    if request.method == "PATCH":
        serializer = TicketUpdateSerializer(
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            try:
                update_ticket(
                    ticket=ticket,
                    changes=serializer.validated_data,
                )
            except InvalidAssigneeError as error:
                return Response({"assigned_to": [str(error)]}, status=400)

            return Response(TicketSerializer(ticket).data)
        return Response(serializer.errors, status=400)

    if request.method == "GET":
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
