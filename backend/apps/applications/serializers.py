from rest_framework import serializers
from .models import Application, AIAnalysis


class AIAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAnalysis
        fields = [
            "id", "score", "skills_score", "experience_score", "education_score",
            "strengths", "weaknesses", "missing_skills", "explanation", "created_at",
        ]
        read_only_fields = fields  # tout est en lecture seule : rempli par l'IA plus tard


class ApplicationSerializer(serializers.ModelSerializer):
    ai_analysis = AIAnalysisSerializer(read_only=True)
    candidate_email = serializers.EmailField(source="candidate.user.email", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id", "candidate", "candidate_email", "job", "job_title",
            "status", "cover_letter", "match_score", "ai_analysis",
            "applied_at", "updated_at",
        ]
        read_only_fields = ["id", "candidate", "match_score", "applied_at", "updated_at"]