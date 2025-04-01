
from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name = 'index')

from django.shortcuts import path, include

# Create your views here.
urlpatterns = [
    path('', include('main.urls'))

]