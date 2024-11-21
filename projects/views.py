from django.shortcuts import redirect,get_object_or_404,render, HttpResponse
from django.views.generic import ListView, DetailView
from .models import Project
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .recommendation_system import recommend_projects

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.object.id
        # Fetch recommended projects
        context['recommended_projects'] = recommend_projects(project_id)
        return context

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

@login_required
def dashboard(request):
    # Get the user's joined projects
    user_projects = Project.objects.filter(volunteers=request.user)
    
    # Get total number of projects
    total_projects = Project.objects.count()
    
    # Get total number of distinct volunteers across all projects
    total_volunteers = Project.objects.values('volunteers').distinct().count()

    # Prepare data for chart visualization (number of volunteers per project)
    project_titles = [project.title for project in Project.objects.all()]
    volunteers_count = [project.volunteers.count() for project in Project.objects.all()]

    context = {
        'user_projects': user_projects,
        'total_projects': total_projects,
        'total_volunteers': total_volunteers,
        'project_titles': project_titles,
        'volunteers_count': volunteers_count,
    }
    
    return render(request, 'projects/dashboard.html', context)

