from django.contrib import admin
from .models import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ["id", "application", "scheduled_at", "status", "duration"]
    list_filter = ["status"]