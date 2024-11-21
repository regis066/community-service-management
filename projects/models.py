from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    volunteers_needed = models.PositiveIntegerField()  # Changed to PositiveIntegerField
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, choices=[
        ('health', 'Health'),
        ('education', 'Education'),
        ('environment', 'Environment'),
        ('community', 'Community')
    ], default="community")
    location = models.CharField(max_length=255, blank=True, null=True, default="Not specified")
    volunteers = models.ManyToManyField(User, related_name='joined_projects', blank=True)

    def __str__(self):
        return self.title
    
    @property
    def volunteers_count(self):
        """Return the count of volunteers for this project."""
        return self.volunteers.count()

    def clean(self):
        """Custom validation for start and end dates."""
        today = date.today()
        
        # Validate the start and end dates
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({'end_date': "End date must be greater than start date."})
        
        # Check if the project is active based on the dates
        if self.start_date and self.end_date:
            self.is_active = self.start_date <= today <= self.end_date
        else:
            self.is_active = False

    def save(self, *args, **kwargs):
        """Override save method to call clean method."""
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)  # Call the original save method
