from django.contrib import admin
from .models import Student, Course, Grade
from .models import CustomUser

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'enrollment_date')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'display_teachers')

    def display_teachers(self, obj):
        return ", ".join(teacher.username for teacher in obj.teachers.all())
    display_teachers.short_description = "Преподаватели"


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'date_received')
    list_filter = ('course',)
    search_fields = ('student__first_name', 'student__last_name', 'course__name')




admin.site.register(CustomUser)
