import uuid
from django.urls import path
from . import views
from projects.schema_graph.views import Schema



urlpatterns =[
    path('', views.home, name='projects/guy'),
    path('myProjects',views.myProjects, name='projects/myProjects'),
    path('editor/<str:pk>',views.editor,name='projects/ediitor>'),
    path("schema/<str:pk>", Schema.as_view,name='schema'),
    path("schema/", Schema.get_project,name='schema'),


    ]