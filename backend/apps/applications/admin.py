from django.contrib import admin
from .models import Application
from .models import Application, AIAnalysis


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["id", "candidate", "job", "status", "match_score", "applied_at"]
    list_filter = ["status"]
    search_fields = ["candidate__user__email", "job__title"]

@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ["id", "application", "score", "created_at"]