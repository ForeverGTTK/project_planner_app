"""
Definition of urls for project_planner_app.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views as app_views  # Import views from 'app' with an alias
from projects import views as projects_views  # Import views from 'polls' with an alias
#from schema_graph.views import Schema

urlpatterns = [
    path('', projects_views.home, name='home'),  # Use 'app_views' for views from 'app'
    
    path('login/',
         LoginView.as_view(
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context={
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    
    path('projects/', include('projects.urls')),
    path('schema/', include('projects.urls')),
    path('contact/', projects_views.contact, name='contact'),
    path('about/', projects_views.about, name='about'),
    path('myProjects/', projects_views.myProjects, name='myProjects'),
    path('editor/<str:pk>', projects_views.editor,name=('editor')),
]
