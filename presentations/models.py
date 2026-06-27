from django.db import models
from django.conf import settings

PRESENTATION_TYPES = [
    ('PROJECT_VIVA', 'Project Viva'),
    ('RESEARCH_SEMINAR', 'Research Seminar'),
    ('STARTUP_PITCH', 'Startup Pitch'),
    ('INTERVIEW_DECK', 'Interview Deck'),
    ('TUTORIAL', 'Tutorial'),
    ('INTERNAL_REVIEW', 'Internal Review'),
]

AUDIENCE_TYPES = [
    ('PROFESSOR', 'Professor'),
    ('HR_RECRUITER', 'HR Recruiter'),
    ('INVESTOR', 'Investor'),
    ('STUDENTS', 'Students'),
    ('ENGINEERS', 'Engineers'),
]

STATUS_CHOICES = [
    ('UPLOADED', 'Uploaded'),
    ('PARSING', 'Parsing'),
    ('GENERATING', 'Generating'),
    ('READY', 'Ready'),
    ('ERROR', 'Error'),
]

class Presentation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='presentations'
    )
    title = models.CharField(max_length=255)
    presentation_type = models.CharField(
        max_length=50, choices=PRESENTATION_TYPES, blank=True
    )
    audience = models.CharField(
        max_length=50, choices=AUDIENCE_TYPES, blank=True
    )
    uploaded_file = models.FileField(
        upload_to='uploads/%Y/%m/', blank=True, null=True
    )
    raw_text = models.TextField(blank=True)
    parsed_content = models.JSONField(default=dict, blank=True)
    slides_data = models.JSONField(default=list, blank=True)
    viva_questions = models.JSONField(default=list, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='UPLOADED'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.user.email}"

    def slide_count(self):
        return len(self.slides_data) if self.slides_data else 0