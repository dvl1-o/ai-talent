from rest_framework import permissions
from .models import Membership


class IsOrganizationMember(permissions.BasePermission):
    """
    Autorise l'accès uniquement si l'utilisateur a un Membership
    dans l'organisation concernée.
    """

    def has_object_permission(self, request, view, obj):
        return Membership.objects.filter(
            user=request.user, organization=obj
        ).exists()