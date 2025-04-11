from django.shortcuts import render, redirect
from .models import Student, Course
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib import messages



@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'education/student_list.html', {'students': students})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна! Вы вошли в систему.")
            return redirect('/accounts/dashboard/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'education/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/accounts/dashboard/')
    else:
        form = AuthenticationForm()
    return render(request, 'education/login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'education/profile.html')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'education/register.html'
    success_url = reverse_lazy('login')


def search_students(request):
    first_name = request.GET.get('first_name', '').strip()
    last_name = request.GET.get('last_name', '').strip()
    course_id = request.GET.get('course', '').strip()

    students = Student.objects.all()

    if first_name:
        students = students.filter(first_name__icontains=first_name)
    if last_name:
        students = students.filter(last_name__icontains=last_name)
    if course_id:
        students = students.filter(grade__course__id=course_id).distinct()

    show_results = bool(first_name or last_name or course_id)

    courses = Course.objects.all()
    context = {
        'students': students if show_results else [],
        'courses': courses,
        'show_results': show_results,
    }
    return render(request, 'education/student_search.html', context)
