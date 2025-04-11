from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.is_teacher:
        return render(request, 'accounts/teacher_dashboard.html')
    elif request.user.is_student:
        return render(request, 'accounts/student_dashboard.html')
    else:
        return render(request, 'accounts/unknown_role.html')
