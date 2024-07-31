"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import Projects,data_container,data_items,container_relation


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/guy.html'
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/contact.html',
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
        'projects/myProjects.html',
        {
            'title':'My projects',
            'projects_list':projects_list,
            'year':datetime.now().year,
        }
    )

def editor(request,pk):
    assert isinstance(request, HttpRequest)
    try:
        containers = []
        root_containers = data_container.objects.filter(project_ID = pk, is_root=True)
        for root in root_containers:
            containers.append(root.get_data())
            for child in root.get_children():
                containers.append(f'__{child.get_data}')
    except:
        containers = ['no data to show yet', 'please insert new data']
        

    return render(
        request,
        'projects/editor.html',
        {
            'title':'My project editor',
            'project_name' : Projects.objects.get(project_ID=pk),
            'container_list': containers,
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/about.html',
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
        'projects/forms/addStep.html',
        context
        )

        