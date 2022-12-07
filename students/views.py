from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import ListView


@method_decorator(login_required, name='dispatch')
class StudentListView(ListView):
    model = User
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    ordering = ['last_name']