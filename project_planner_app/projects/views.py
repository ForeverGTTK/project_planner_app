"""
Definition of views.
"""
import os,re
from datetime import datetime, timedelta
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.db.models import Count
from .models import *
from .forms import DataContainerForm,newProjectForm,existingProjectForm
from typing import Dict


def retrender(request,page_address,context):
    context.__setitem__('easterEgg',True if datetime.now().minute%2==0 else False)
    # operations on elements to add
    app_name = re.split(r'_|(?=[A-Z])', os.path.splitext(os.path.basename(page_address))[0])

    if context['easterEgg']:
        title = ' '.join(word.capitalize() for word in app_name)
    else:
        title= ' '.join(word.lower() for word in app_name)
    
    # appending items to page context
    context.__setitem__('title',str(title))  
    context.__setitem__('year',datetime.now().year)

    return render(
        request,
        page_address,
        context
        )


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return retrender(
        request,
        'projects/pages/home.html',
        {}
    )


def myProjects(request):
    """Renders the myProjects page."""
    assert isinstance(request, HttpRequest)
    projects_list = Projects.objects.filter(owner_ID= request.user)
    topics = Topics.objects.all()
    return retrender(
        request,
        'projects/pages/myProjects.html',
        {
            'projects_list':projects_list,
            'topics':topics,
        }
    )

def exploreProjects(request,sort_by='Topic'):
    """Renders the myProjects page."""
    assert isinstance(request, HttpRequest)
    projects_list = Projects.objects.filter(is_public= True)
    if sort_by == 'owner_ID':
        sorted_projects = sort_projects_by(project_list=projects_list,attr_name='owner_ID')
    elif sort_by=='name':
        sorted_projects = sort_projects_by(project_list=projects_list,attr_name='name')
    elif sort_by == 'Topic':
        sorted_projects = sort_projects_by(project_list=projects_list,attr_name='Topic')
    else:
        sorted_projects = sort_projects_by(project_list=projects_list)
    topics = Topics.objects.all()
    return retrender(
        request,
        'projects/pages/exploreProjects.html',
        {
            'projects_list':projects_list,
            'sorted_projects':sorted_projects,
            'sorted_by':sort_by,
            'topics':topics,
        }
    )

def editor(request, pk):
    assert isinstance(request, HttpRequest)
    try:
        # Fetch the project
        project = Projects.objects.get(ID=pk)
         
        topics = Topics.get_project_topics(project_id=pk)
        # Get the dependency tree
        tree = project.build_dep_tree()

    except Exception as e:
        tree = {}
        print(f'Error: {e}')

    return retrender(
        request,
        'projects/pages/editor.html',
        {
            'project': project,
            'topics':topics,
            'tree': tree,
        }
    )

def projectView(request, pk):
   assert isinstance(request, HttpRequest)
   try:
        # Fetch the project
        project = Projects.objects.get(ID=pk)
         
        topics = Topics.get_project_topics(project_id=pk)

        # Get the dependency tree
        tree = project.build_dep_tree()

        # Assuming day 0 is project created_at date, calculate day list
        day_list = [i for i in range(1, 31)]

   except Exception as e:
        tree = {}
        day_list = []
        print(f'Error: {e}')

   return retrender(
        request,
        'projects/pages/projectView.html',
        {
            'project': project,
            'topics':topics,
            'tree': tree,
            'day_list': day_list,
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
    return retrender(request, 'projects/pages/forms/addProject.html', context)


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
    return retrender(request, 'projects/pages/forms/addContainer.html', context)


def updateProject(request,pk):
    editable_project = Projects.objects.get(ID=pk)

    if request.method == 'POST':
        form = existingProjectForm(request.POST,instance=editable_project)
        if form.is_valid():
            project = form.save(commit=False)
            #add operations to edit automaticly
            project.save()

            return redirect('myProjects')
    else:
        form = existingProjectForm(instance=editable_project)

    context = {
        'form': form,
      
    }
    return retrender(request, 'projects/pages/forms/addProject.html', context)

def updateContainer(request,project_pk,container_pk=None):
    """
    to be written
    """
    if container_pk ==None:
        return addContainer(request=request,project_pk=project_pk)
    project = get_object_or_404(Projects, pk=project_pk)
    form = DataContainerForm(project = project)
    container = data_container.objects.get(ID=container_pk)
    context = {
        'form': form,
        'project': project,
        'container': container,
    }
    return retrender(request, 'projects/pages/forms/addContainer.html', context)    

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


def userPage(request,userName):
    """Renders the User page."""
    assert isinstance(request, HttpRequest)
    selected_user=  User.objects.get(username=userName)
    user_details= {
        'UserName':userName,
        'Name':selected_user.get_full_name,
        'mail':selected_user.email,
        'owned projects':Projects.objects.filter(owner_ID=selected_user),
        'Registered Since':selected_user.date_joined.date
        }
    return render(
        request,
        'projects/pages/user.html',
        {
            'title':userName,
            'message':user_details,
            'year':datetime.now().year,
        }
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
