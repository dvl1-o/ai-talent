from django.contrib import admin
from .models import Candidate, Resume, Skill, CandidateSkill



@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "location", "created_at"]
    search_fields = ["user__email"]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["id", "file_name", "candidate", "parsing_status", "created_at"]
    list_filter = ["parsing_status"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category"]
    search_fields = ["name"]


@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    list_display = ["id", "candidate", "skill", "level", "years_experience"]