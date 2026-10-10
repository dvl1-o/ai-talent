import os
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"]
MAX_FILE_SIZE_MB = 5


def validate_resume_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file extension '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if file.size > max_size_bytes:
        raise ValidationError(
            f"File too large ({file.size / (1024*1024):.1f} MB). Max allowed: {MAX_FILE_SIZE_MB} MB"
        )