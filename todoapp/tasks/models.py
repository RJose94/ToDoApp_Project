from django.db import models
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pendiente'),
        ('C', 'Completado'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return self.title