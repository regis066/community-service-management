from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from django.utils import timezone

class ServiceHour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now())

    def __str__(self):
        return f"{self.user.username} - {self.hours} hours for {self.project.title}"
