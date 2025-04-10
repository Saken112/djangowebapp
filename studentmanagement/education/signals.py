from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Student, Teacher

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            Student.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)
        elif instance.role == 'teacher':
            Teacher.objects.create(user=instance)
