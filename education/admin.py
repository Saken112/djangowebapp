from django.contrib import admin
from .models import Student, Course, Grade
from .models import CustomUser

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Grade)
admin.site.register(CustomUser)
