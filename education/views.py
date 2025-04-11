from django.shortcuts import render, redirect
from .models import Student, Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm



@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'education/student_list.html', {'students': students})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_list')
    else:
        form = UserCreationForm()
    return render(request, 'education/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_list')
            else:
                form.add_error(None, 'Неверные данные')
    else:
        form = AuthenticationForm()
    return render(request, 'education/login.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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