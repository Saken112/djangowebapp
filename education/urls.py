from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
