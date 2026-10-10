from django.db import models

# Create your models here.
from django.db import models
from apps.candidates.models import Candidate
from apps.jobs.models import Job


class Application(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under review"
        SHORTLISTED = "SHORTLISTED", "Shortlisted"
        INTERVIEW = "INTERVIEW", "Interview"
        REJECTED = "REJECTED", "Rejected"
        HIRED = "HIRED", "Hired"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SUBMITTED
    )
    cover_letter = models.TextField(blank=True)
    match_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "job"],
                name="unique_candidate_job_application",
            )
        ]

    def __str__(self):
        return f"{self.candidate.user.email} → {self.job.title} ({self.status})"

class AIAnalysis(models.Model):
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="ai_analysis",
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skills_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    experience_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    education_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Analysis - {self.application}"