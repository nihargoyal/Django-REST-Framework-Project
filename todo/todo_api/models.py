from django.db import models


# Create your models here.
class ToDo(models.Model):
    priority=models.IntegerField(unique=True)
    task=models.CharField(max_length=600)
    completed=models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.task