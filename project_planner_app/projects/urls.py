import uuid
from django.urls import path
from . import views



urlpatterns =[
    path('', views.home, name='projects/guy'),
    path('myProjects',views.myProjects, name='projects/myProjects'),
    path('editor/<str:pk>',views.editor,name='projects/ediitor'),
    path('addContainer',views.addContainer,name='addContainer'),
    path('addContainer/<str:project_pk>/<str:parent_pk>/', views.addContainer, name='addContainerTo'),

    ]