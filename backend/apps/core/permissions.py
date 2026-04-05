from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.users.models import Role

class IsAdmin(BasePermission):
    """Only users with role=admin can pass."""
    message = "Admin access required."

    def has_permission(self, request, view):
        
        return (
            request.user.is_authenticated
            and request.user.role == Role.ADMIN
        )


class IsAnalystOrAbove(BasePermission):
    """Analysts and admins can pass. Viewers cannot."""
    message = "Analyst or Admin access required."

    def has_permission(self, request, view):
        allowed = {Role.ANALYST, Role.ADMIN}
        return (
            request.user.is_authenticated
            and request.user.role in allowed
        )


class IsOwnerOrAdmin(BasePermission):
    """Owner or Admin can pass"""
    message = "You do not have access to this resource."

    def has_object_permission(self, request, view, obj):
        if request.user.role == Role.ADMIN:
            return True
        return obj.user == request.user
