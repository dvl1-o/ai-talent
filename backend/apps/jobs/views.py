from rest_framework import viewsets, permissions
from apps.organizations.models import Membership
from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne voit que les jobs des organisations dont il est membre
        user_orgs = Membership.objects.filter(
            user=self.request.user
        ).values_list("organization_id", flat=True)
        return Job.objects.filter(organization_id__in=user_orgs)

    def perform_create(self, serializer):
        # Sécurité : on vérifie que l'utilisateur est bien membre
        # de l'organisation qu'il essaie d'utiliser pour créer le job
        organization = serializer.validated_data["organization"]
        is_member = Membership.objects.filter(
            user=self.request.user, organization=organization
        ).exists()
        if not is_member:
            raise permissions.PermissionDenied(
                "You are not a member of this organization."
            )
        serializer.save()