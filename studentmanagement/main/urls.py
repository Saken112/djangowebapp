from django.shortcuts import path, include

# Create your views here.
urlpatterns = [
    path('', include('main.urls'))
]