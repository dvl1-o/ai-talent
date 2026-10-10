from rest_framework import serializers
from .models import Organization, Membership


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "description", "website", "logo", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class MembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Membership
        fields = ["id", "user", "user_email", "organization", "role", "created_at"]
        read_only_fields = ["id", "created_at"]