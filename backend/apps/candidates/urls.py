from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, ResumeViewSet, SkillViewSet

router = DefaultRouter()
router.register("candidates", CandidateViewSet, basename="candidate")
router.register("resumes", ResumeViewSet, basename="resume")
router.register("skills", SkillViewSet, basename="skill")

urlpatterns = router.urls