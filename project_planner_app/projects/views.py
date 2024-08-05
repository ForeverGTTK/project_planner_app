"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.db.models import Count
from .models import Projects,data_container,data_items,container_relation
from .forms import DataContainer
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


def addContainer(request):
    form = DataContainer()
    if request.method == 'POST':
        form = DataContainer(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myProjects')
    context = {'form':form}
    return render(
        request,
        'projects/pages/forms/addContainer.html',
        context
        )

        