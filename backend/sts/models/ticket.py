from django.conf import settings
from django.db import models


class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class TicketStatus(models.TextChoices):
        SIN_ASIGNAR = "SIN_ASIGNAR", "Unassigned"
        ASIGNADA = "ASIGNADA", "Asignada"
        ACTUALIZADO = "ACTUALIZADO", "Actualizado"
        PERSISTE = "PERSISTE", "Persiste"
        CLARIFICATION = "CLARIFICATION", "Clarification"
        CORREGIDA = "CORREGIDA", "Corregida"

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    ticket_status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.SIN_ASIGNAR,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True,
        blank=True,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets",
        null=True,
        blank=True,
    )
