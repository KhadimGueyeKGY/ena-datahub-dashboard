from django.shortcuts import render
 
from Home.main import app as dash_app


def dash_view(request):
        return render(request, 'home.html')
