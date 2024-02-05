from django.db import models

from ham_code_digikala.presentations.models import Presentation


class Slide(models.Model):
    section_link = models.CharField(max_length=255)
    section_id = models.CharField(max_length=150)
    content = models.TextField()
    presentation_id = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
