from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ticket_comments_read_create,
    ticket_details_update,
    ticket_list_create,
)

urlpatterns = [
    path("tickets/", ticket_list_create, name="ticket_list_create"),
    path(
        "tickets/<int:pk>/",
        ticket_details_update,
        name="ticket_details_update",
    ),
    path(
        "tickets/<int:pk>/comments/",
        ticket_comments_read_create,
        name="ticket_comments_read_create",
    ),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
