from django.db import models

# Create your models here.

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


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)