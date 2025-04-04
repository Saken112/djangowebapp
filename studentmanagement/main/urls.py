from django.urls import path, include
from main import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('students/', views.student_list, name='student_list')

]





