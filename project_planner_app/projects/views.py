"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.db.models import Count
from .models import Projects,data_container,data_items,container_relation
from .forms import DataContainerForm
from typing import Dict

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/pages/guy.html'
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/pages/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def myProjects(request):
    """Renders the myProjects page."""
    assert isinstance(request, HttpRequest)
    projects_list = Projects.objects.all()
    return render(
        request,
        'projects/pages/myProjects.html',
        {
            'title':'My projects',
            'projects_list':projects_list,
            'year':datetime.now().year,
        }
    )
def editor(request, pk):
    assert isinstance(request, HttpRequest)
    try:
        # Fetch the project
        project = Projects.objects.get(ID=pk)
         
        # Get the dependency tree
        tree = project.build_dep_tree()

    except Exception as e:
        tree = {}
        print(f'Error: {e}')

    return render(
        request,
        'projects/pages/editor.html',
        {
            'title': 'Project Editor',
            'project': project,
            'tree': tree,
            'year': datetime.now().year,
        }
    )



def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/pages/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def addContainer(request, project_pk=None, parent_pk=None):
    project = get_object_or_404(Projects, pk=project_pk)
    parent_container = None
    if parent_pk:
        parent_container = get_object_or_404(data_container, pk=parent_pk)

    if request.method == 'POST':
        form = DataContainerForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            container.project_ID = project
            container.created_by = request.user
            if parent_pk:
                container.is_root = False
            container.level = parent_container.level + 1 if parent_container else 0
            container.save()
            if parent_container:
                container_relation.objects.create(
                    project_ID=project,
                    parent=parent_container,
                    child=container
                )
            return redirect('myProjects')
    else:
        form = DataContainerForm()

    context = {
        'form': form,
        'project': project,
        'parent_container': parent_container,
    }
    return render(request, 'projects/pages/forms/addContainer.html', context)