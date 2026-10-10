from rest_framework import permissions
from apps.organizations.models import Membership


class CanAccessApplication(permissions.BasePermission):
    """
    Autorise l'accès si :
    - l'utilisateur est le candidat propriétaire de la candidature, OU
    - l'utilisateur est membre de l'organisation propriétaire du job
    """

    def has_object_permission(self, request, view, obj):
        is_owner = obj.candidate.user == request.user
        is_org_member = Membership.objects.filter(
            user=request.user, organization=obj.job.organization
        ).exists()
        return is_owner or is_org_member