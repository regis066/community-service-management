from django.shortcuts import redirect,get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Project
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

@login_required
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Check if the user is already a volunteer
    if project.volunteers.filter(id=request.user.id).exists():
        messages.error(request, 'You are already a volunteer for this project.')
    else:
        project.volunteers.add(request.user)
        messages.success(request, f'You have joined the project: {project.title}')
    
    return redirect('project_detail', pk=project.id)  # Redirect to the project detail page


