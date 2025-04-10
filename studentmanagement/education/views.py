from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView
from .models import Student, Teacher, CustomUser
from .forms import CustomUserCreationForm
from .models import Course, Grade

@login_required
def student_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        students = Student.objects.all()
    return render(request, 'education/student_list.html', {'students': students})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
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
                if user.role == 'student':
                    return redirect('student_dashboard')
                elif user.role == 'teacher':
                    return redirect('teacher_dashboard')
                return redirect('profile')
            else:
                form.add_error(None, 'Неверные данные для входа')
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

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('profile')
    student = get_object_or_404(Student, user=request.user)
    courses = Course.objects.filter(students=student)
    grades = Grade.objects.filter(student=student)
    return render(request, 'dashboard/student.html', {
        'student': student,
        'courses': courses,
        'grades': grades,
    })

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('profile')
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    return render(request, 'dashboard/teacher.html', {
        'teacher': teacher,
        'courses': courses,
    })
