from django.db import models


from accounts.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Presentation(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    background = models.ImageField(upload_to='images/')
    is_published = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag)

    def delete(self, using=None, keep_parents=False):
        self.background.storage.delete(str(self.background.name))

    def __str__(self):
        format_datetime = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.title} created at {format_datetime}'
