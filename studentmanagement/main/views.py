from django.shortcuts import render
from django.http import HttpResponse
from education.models import Student

def index(request):
    return render(request, 'main/maintemp.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'education/student_list.html', {'students': students})





