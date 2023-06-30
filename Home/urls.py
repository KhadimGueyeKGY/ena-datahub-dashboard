from django.urls import path 
from . import views

urlpatterns = [
    #path('', views.dash_view, name='ena-data-dashboard'),
    path('ena-data-dashboard/', views.dash_view, name='ena-data-dashboard')
]