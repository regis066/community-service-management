# service_hours/forms.py
from django import forms
from .models import ServiceHour, Project

class ServiceHourForm(forms.ModelForm):
    class Meta:
        model = ServiceHour
        fields = ['project', 'hours', 'date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the current user
        super().__init__(*args, **kwargs)
        if user:
            # Limit the queryset to projects the user is involved in
            self.fields['project'].queryset = Project.objects.filter(volunteers=user)
