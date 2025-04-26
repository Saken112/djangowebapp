from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField(auto_now_add=True)

    def final_grade_for_course(self, course):
        GRADE_WEIGHTS = {
            'exam': Decimal('0.5'),
            'project': Decimal('0.3'),
            'quiz': Decimal('0.1'),
            'homework': Decimal('0.1'),
            'other': Decimal('0.1'),
        }

        grades = self.grade_set.filter(course=course)
        if grades.exists():
            weighted_sum = Decimal('0')
            total_weight = Decimal('0')

            for g in grades:
                weight = GRADE_WEIGHTS.get(g.grade_type, Decimal('0.1'))
                weighted_sum += g.grade * weight
                total_weight += weight

            return round(weighted_sum / total_weight, 2) if total_weight else None

        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    teachers = models.ManyToManyField(  # <-- Изменение здесь!
        settings.AUTH_USER_MODEL,
        blank=True,
        limit_choices_to={'is_teacher': True},
        related_name='courses'
    )

    def __str__(self):
        return self.name


class Grade(models.Model):
    GRADE_TYPE_CHOICES = [
        ('exam', 'Экзамен'),
        ('quiz', 'Тест'),
        ('project', 'Проект'),
        ('homework', 'Домашка'),
        ('other', 'Другое'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPE_CHOICES, default='other')
    weight = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('10.0'))]
    )
    comments = models.TextField(blank=True, null=True)
    date_received = models.DateField(auto_now_add=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_teacher': True},
        related_name='given_grades'
    )

    class Meta:
        unique_together = ('student', 'course', 'grade_type')

    def __str__(self):
        return f"{self.student} - {self.course} ({self.grade_type}): {self.grade}"
