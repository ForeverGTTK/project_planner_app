"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Count
from .models import Projects,data_container,data_items,container_relation


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
        project = Projects.objects.get(ID=pk)
        containers = data_container.objects.filter(project_ID=project)
        relations = container_relation.objects.filter(project_ID=project)
        
        # Annotate containers with the number of children
        containers = containers.annotate(child_count=Count('child_relations'))

        # Build level dictionary
        level_dict = {}
        for container in containers:
            level_dict.setdefault(container.level, []).append(container)
        
    except Exception as e:
        containers = []
        relations = []
        level_dict = {}
        print(f'Error: {e}')

    return render(
        request,
        'projects/pages/editor.html',
        {
            'title': 'Project Editor',
            'project': project,
            'level_dict': level_dict,
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


def addStep(request):
    
    context = {}
    return render(
        request,
        'projects/pages/forms/addStep.html',
        context
        )

        