import uuid
from django.urls import path
from . import views



urlpatterns =[
    path('', views.home, name='projects/guy'),
    path('user/<str:userName>',views.userPage,name='userPage'),
    

    path('myProjects/',views.myProjects, name='myProjects'),
    path('exploreProjects/', views.exploreProjects, name='exploreProjects'),
    path('exploreProjects/<str:sort_by>', views.exploreProjects, name='exploreProjects'),


    path('editor/<str:pk>',views.editor,name='projects/ediitor'),
    path('projectView/<str:pk>',views.projectView,name='projectView'),

    path('addContainer/',views.addContainer,name='addContainer'),
    path('addContainer/<str:project_pk>/', views.addContainer, name='addRootContainer'),
    path('addContainer/<str:project_pk>/<str:parent_pk>/', views.addContainer, name='addContainerTo'),
    

    path('updateProject/<str:pk>',views.updateProject,name='updateProject'),
    path('updateContainer/<str:project_pk>',views.updateContainer,name='updateaddContainer'),
    path('updateContainer/<str:project_pk>/<str:container_pk>',views.updateContainer,name='updateContainer'),


    path('addProject/',views.addProject,name='addProject'),

       
    path('contact/', views.contact, name='contact'),
    path('about/',views.about, name='about'),
    ]