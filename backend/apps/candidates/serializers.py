from rest_framework import serializers
from .models import Candidate, Resume, Skill, CandidateSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category"]


class CandidateSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True)

    class Meta:
        model = CandidateSkill
        fields = ["id", "skill", "skill_name", "level", "years_experience"]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id", "file", "file_name", "parsed_text",
            "parsing_status", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "file_name", "parsed_text", "parsing_status", "created_at", "updated_at"]




class CandidateSerializer(serializers.ModelSerializer):
    resumes = ResumeSerializer(many=True, read_only=True)
    candidate_skills = CandidateSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id", "user", "phone", "location", "bio",
            "linkedin_url", "github_url", "resumes", "candidate_skills",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]