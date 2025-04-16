from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from .models import Grade, Course


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label="Роль")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birth_date', 'profile_image', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        user.is_student = role == 'student'
        user.is_teacher = role == 'teacher'
        if commit:
            user.save()
            if user.is_student:
                Student.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email
                )
        return user

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)