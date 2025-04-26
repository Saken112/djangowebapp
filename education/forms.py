from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Grade, Course


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label="Роль")

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'birth_date', 'profile_image', 'password1', 'password2', 'role'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_student = role == 'student'
        user.is_teacher = role == 'teacher'
        if commit:
            user.save()
            if user.is_student and not hasattr(user, 'student'):
                Student.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email
                )
        return user


class GradeForm(forms.ModelForm):
    GRADE_WEIGHTS = {
        'exam': 0.5,
        'project': 0.3,
        'quiz': 0.1,
        'homework': 0.1,
        'other': 0.1,
    }

    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade_type', 'grade', 'comments']
        widgets = {
            'grade': forms.NumberInput(attrs={'step': '0.01', 'min': 0, 'max': 100}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs['class'] = 'form-control'

        self.fields['grade_type'].widget.attrs['class'] = 'form-select'
        self.fields['student'].widget.attrs['class'] = 'form-select'
        self.fields['course'].widget.attrs['class'] = 'form-select'

        if user and user.is_teacher:
            self.fields['course'].queryset = Course.objects.filter(teachers=user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.weight = self.GRADE_WEIGHTS.get(instance.grade_type, 0.1)
        if commit:
            instance.save()
        return instance


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birth_date', 'profile_image']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
