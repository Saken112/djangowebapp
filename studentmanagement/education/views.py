from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Student
from .forms import CustomUserCreationForm
from django.db.models import Q
from django.views.generic.edit import CreateView


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
