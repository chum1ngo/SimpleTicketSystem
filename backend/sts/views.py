from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer, CommentSerializer

@api_view(["GET", "POST"])
def ticket_list_create(request):
    if request.method == "POST":
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    if request.method == "GET":
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


@api_view(["GET", "PATCH"])
def ticket_details_update(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)

    if request.method == "PATCH":
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "GET":
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

@api_view(["GET", "POST"])
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