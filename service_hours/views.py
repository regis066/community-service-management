from django.shortcuts import render, redirect
from .models import ServiceHour
from .forms import ServiceHourForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.models import Project

@login_required
def log_service_hour(request, project_id=None):
    if request.method == 'POST':
        form = ServiceHourForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                service_hour = form.save(commit=False)
                service_hour.user = request.user  # Assign the logged-in user
                service_hour.save()  # Save the service hour instance
                messages.success(request, 'Service hours logged successfully!')
                return redirect('view_logged_hours')  # Redirect to view logged hours after logging
            except Exception as e:
                print(f"Error saving service hour: {e}")  # Print the error for debugging
                messages.error(request, 'An error occurred while logging service hours.')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        # Initialize the form with user info and set the project ID if provided
        form = ServiceHourForm(user=request.user)
        if project_id:  # If a project ID is provided, set it in the form
            form.fields['project'].initial = project_id

    projects = Project.objects.all()  # Fetch all projects
    return render(request, 'service_hours/log_service_hour.html', {'form': form, 'projects': projects})  # Pass projects to the template

@login_required
def view_logged_hours(request):
    logged_hours = ServiceHour.objects.filter(user=request.user)  # Get logged hours for the user
    return render(request, 'service_hours/view_logged_hours.html', {'logged_hours': logged_hours})
