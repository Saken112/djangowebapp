from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('students/search/', views.search_students, name='search_students'),
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/add/', views.add_grade, name='add_grade'),
]
