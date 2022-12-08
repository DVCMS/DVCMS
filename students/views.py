from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from auth.roles import is_lecturer
from students.forms import StudentForm


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_lecturer), name='dispatch')
class StudentListView(ListView):
    model = User
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    ordering = ['last_name']


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_lecturer), name='dispatch')
class StudentCreateView(CreateView):
    model = User
    template_name = 'students/student_create.html'
    form_class = StudentForm
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        students = Group.objects.get(name='student')
        form.instance.save()
        form.instance.groups.add(students)
        return super(StudentCreateView, self).form_valid(form)
