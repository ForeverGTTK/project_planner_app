from os import name
from django.shortcuts import render

from django.http import HttpResponse

text = "test the website\n unfortunally doesnt work in hebrew"

def index(request):
    return render(request,'guy.html',{'header':'ForeverGTTK','content':text})

# Create your views here.
