from django.contrib import admin
from .models import Job, JobSkill


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "organization", "status", "employment_type", "created_at"]
    list_filter = ["status", "employment_type"]
    search_fields = ["title", "organization__name"]


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ["id", "job", "skill", "required", "importance"]
    list_filter = ["required"]