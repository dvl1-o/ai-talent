from django.conf import settings
from django.db import models
from .validators import validate_resume_file

class Candidate(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Resume(models.Model):
    class ParsingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="resumes",
    )
    file = models.FileField(
        upload_to="resumes/%Y/%m/",
        validators=[validate_resume_file],  
    )
    file_name = models.CharField(max_length=255, blank=True)
    parsed_text = models.TextField(blank=True)
    parsing_status = models.CharField(
        max_length=20, choices=ParsingStatus.choices, default=ParsingStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_name} - {self.candidate.user.email}"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CandidateSkill(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_skills",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="candidate_skills",
    )
    level = models.CharField(max_length=50, blank=True)
    years_experience = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "skill"],
                name="unique_candidate_skill",
            )
        ]

    def __str__(self):
        return f"{self.candidate.user.email} - {self.skill.name}"