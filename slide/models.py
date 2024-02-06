from django.db import models

from config.models import BaseModel
from presentation.models import Presentation


class Slide(BaseModel):
    section_link = models.CharField(max_length=255)
    section_id = models.CharField(max_length=150)
    content = models.TextField()
    presentation_id = models.ForeignKey(Presentation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Slide'
