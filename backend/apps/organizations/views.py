from rest_framework import viewsets, permissions
from .models import Organization, Membership
from .serializers import OrganizationSerializer, MembershipSerializer
from .permissions import IsOrganizationMember


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne voit que les organisations dont il est membre
        return Organization.objects.filter(memberships__user=self.request.user)

    def perform_create(self, serializer):
        organization = serializer.save()
        # Celui qui crée l'organisation en devient automatiquement ADMIN
        Membership.objects.create(
            user=self.request.user,
            organization=organization,
            role=Membership.Role.ADMIN,
        )


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne voit que les memberships des organisations
        # dont il fait lui-même partie
        return Membership.objects.filter(
            organization__memberships__user=self.request.user
        ).distinct()