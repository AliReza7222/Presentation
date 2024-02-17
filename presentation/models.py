from django.db import models

from config.models import BaseModel
from user.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Tag'

    def __str__(self):
        return self.name


class Presentation(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    background = models.ImageField(upload_to='images/presentation/')
    is_published = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    presenter = models.CharField(max_length=150, null=True)
    cnt_view = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def increment_views_count(self):
        self.cnt_view += 1
        self.save()

    class Meta:
        db_table = 'Presentation'

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.background.storage.delete(str(self.background.name))
        return super(Presentation, self).delete(*args, **kwargs)

    def __str__(self):
        format_datetime = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.title} created at {format_datetime}'
