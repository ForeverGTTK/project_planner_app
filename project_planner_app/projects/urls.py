import uuid
from django.urls import path
from . import views
from projects.schema_graph.views import Schema



urlpatterns =[
    path('', views.home, name='projects/guy'),
    path('myProjects',views.myProjects, name='projects/myProjects'),
    #path('<str:pk>/',views.editor,name='/editor'),
    path('editor/',views.editor,name='/editor'),
    path("schema/", Schema.as_view(),name='schema'),


    ]