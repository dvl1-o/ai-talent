from django.db.models import Q
from rest_framework import viewsets, permissions, status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.candidates.models import Candidate
from apps.organizations.models import Membership
from apps.ai.services.matching import match_candidate_to_job, calculate_final_score
from .models import Application, AIAnalysis
from .serializers import ApplicationSerializer, AIAnalysisSerializer
from .permissions import CanAccessApplication


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, CanAccessApplication]

    def get_queryset(self):
        user = self.request.user
        user_orgs = Membership.objects.filter(user=user).values_list(
            "organization_id", flat=True
        )
        # Un utilisateur voit :
        # - ses propres candidatures (en tant que candidat)
        # - OU les candidatures sur les jobs de ses organisations (en tant que recruteur)
        return Application.objects.filter(
            Q(candidate__user=user) | Q(job__organization_id__in=user_orgs)
        ).distinct()

    def perform_create(self, serializer):
        candidate = Candidate.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)

    @action(detail=True, methods=["post"], url_path="analyze")
    def analyze(self, request, pk=None):
        """Run AI matching analysis for a given application and persist the result."""
        application = self.get_object()
        candidate = application.candidate
        job = application.job

        # --- Build candidate profile text ---
        profile_parts = []
        if candidate.bio:
            profile_parts.append(candidate.bio)

        # Use the most recently parsed resume if available
        latest_resume = (
            candidate.resumes.filter(parsing_status="COMPLETED")
            .order_by("-created_at")
            .first()
        )
        if latest_resume and latest_resume.parsed_text:
            profile_parts.append(latest_resume.parsed_text)

        # Append candidate skills
        candidate_skills = candidate.candidate_skills.select_related("skill").all()
        if candidate_skills.exists():
            skill_lines = []
            for cs in candidate_skills:
                line = cs.skill.name
                if cs.level:
                    line += f" ({cs.level})"
                if cs.years_experience:
                    line += f" — {cs.years_experience} yr(s)"
                skill_lines.append(line)
            profile_parts.append("Skills: " + ", ".join(skill_lines))

        candidate_profile_text = (
            "\n\n".join(profile_parts) or "No profile information available."
        )

        # --- Job details ---
        job_description = f"{job.title}\n\n{job.description}"
        required_skills = list(
            job.job_skills.filter(required=True).values_list("skill__name", flat=True)
        )

        # --- Call the AI matching service ---
        try:
            result = match_candidate_to_job(
                candidate_profile_text, job_description, required_skills
            )
            final_score = calculate_final_score(result)
        except Exception as exc:
            return Response(
                {"error": f"AI analysis failed: {exc}"},
                status=http_status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # --- Persist / update the AIAnalysis record ---
        analysis, _ = AIAnalysis.objects.update_or_create(
            application=application,
            defaults={
                "score": final_score,
                "skills_score": result.skills_score,
                "experience_score": result.experience_score,
                "education_score": result.education_score,
                "strengths": result.strengths,
                "weaknesses": result.weaknesses,
                "missing_skills": result.missing_skills,
                "explanation": result.explanation,
            },
        )

        # Keep match_score on the Application in sync
        application.match_score = final_score
        application.save(update_fields=["match_score"])

        return Response(AIAnalysisSerializer(analysis).data, status=http_status.HTTP_200_OK)