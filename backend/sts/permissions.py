from rest_framework.permissions import BasePermission, SAFE_METHODS

from .roles import UserRole, get_user_role


class IsDeveloperOrQAOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return get_user_role(request.user) in {
            UserRole.DEVELOPER,
            UserRole.QA,
        }
