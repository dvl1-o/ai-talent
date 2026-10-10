from rest_framework import viewsets, permissions
from .models import Candidate, Resume, Skill, CandidateSkill
from .serializers import CandidateSerializer, ResumeSerializer, SkillSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.ai.services.cv_parser import extract_text_from_pdf, parse_cv_text


class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne voit et ne modifie que SON PROPRE profil candidat
        return Candidate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from rest_framework.parsers import MultiPartParser, FormParser


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Resume.objects.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        candidate = Candidate.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)
    @action(detail=True, methods=["post"])
    def parse(self, request, pk=None):
        resume = self.get_object()
        resume.parsing_status = Resume.ParsingStatus.PROCESSING
        resume.save(update_fields=["parsing_status"])

        try:
            text = extract_text_from_pdf(resume.file)
            resume.parsed_text = text

            cv_data = parse_cv_text(text)

            for skill_name in cv_data.skills:
                skill = Skill.objects.filter(name__iexact=skill_name).first()
                if not skill:
                    skill = Skill.objects.create(name=skill_name)
                CandidateSkill.objects.get_or_create(
                    candidate=resume.candidate, skill=skill
                )

            resume.parsing_status = Resume.ParsingStatus.COMPLETED
            resume.save()

            return Response({
                "parsing_status": resume.parsing_status,
                "structured_data": cv_data.model_dump(),
            })

        except Exception as e:
            resume.parsing_status = Resume.ParsingStatus.FAILED
            resume.save(update_fields=["parsing_status"])
            return Response({"error": str(e)}, status=500)


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    # Les Skills sont une donnée partagée/normalisée (section 18 du doc) :
    # tout le monde peut les consulter, mais pas les créer/modifier via cette API
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]