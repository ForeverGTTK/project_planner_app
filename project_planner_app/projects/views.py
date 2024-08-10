"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.db.models import Count
from .models import Projects,data_container,data_items,container_relation
from .forms import DataContainerForm,newProjectForm
from typing import Dict

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'projects/pages/guy.html'
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


def addProject(request):


    if request.method == 'POST':
        form = newProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner_ID = request.user
            project.created_by = request.user
            project.save()

            return redirect('myProjects')
    else:
        form = newProjectForm()

    context = {
        'form': form,
      
    }
    return render(request, 'projects/pages/forms/addProject.html', context)


def addContainer(request, project_pk=None, parent_pk=None):
    project = get_object_or_404(Projects, pk=project_pk)
    parent_container = None
    if parent_pk:
        parent_container = get_object_or_404(data_container, pk=parent_pk)

    if request.method == 'POST':
        form = DataContainerForm(request.POST,project = project)
        if form.is_valid():
            container = form.save(commit=False)
            container.project_ID = project
            container.created_by = request.user
            
            # Handling root and level assignment
            if parent_pk:
                container.is_root = False
                container.level = parent_container.level + 1
            else:
                container.is_root = True
                container.level = 0

            if container.prequisit:
                container.level = container.prequisit.level + 1
            
            container.save()

            if parent_container:
                container_relation.objects.create(
                    created_by=request.user,
                    project_ID=project,
                    parent=parent_container,
                    child=container
                )

            return redirect('myProjects')
    else:
        form = DataContainerForm(project = project)

    context = {
        'form': form,
        'project': project,
        'parent_container': parent_container,
    }
    return render(request, 'projects/pages/forms/addContainer.html', context)

#TODO dodododo !!!
"""
TODO generate a delete function
TODO filter projects by accsess
TODO add tags to projects
TODO add view more objects
TODO add item editor
TODO figure time and duration planing
TODO add budget costs 
"""



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
