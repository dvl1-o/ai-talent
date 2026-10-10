from rest_framework import serializers
from .models import Job, JobSkill


class JobSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True)

    class Meta:
        model = JobSkill
        fields = ["id", "skill", "skill_name", "required", "importance"]


class JobSerializer(serializers.ModelSerializer):
    job_skills = JobSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = [
            "id", "organization", "title", "description", "location",
            "employment_type", "experience_level", "salary_min", "salary_max",
            "status", "deadline", "job_skills", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]