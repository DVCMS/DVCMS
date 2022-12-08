from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from auth.roles import is_lecturer


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_lecturer), name='dispatch')
class StudentListView(ListView):
    model = User
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    ordering = ['last_name']
