from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from auth.roles import is_lecturer
from lectures.forms import LectureForm
from lectures.models import Lecture


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_lecturer), name='dispatch')
class LectureListView(ListView):
    model = Lecture
    template_name = 'lectures/lecture_list.html'
    context_object_name = 'lectures'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_lecturer), name='dispatch')
class LectureCreateView(CreateView):
    model = Lecture
    template_name = 'lectures/lecture_create.html'
    form_class = LectureForm
    success_url = reverse_lazy('lectures:lecture_list')

    def form_valid(self, form):
        form.instance.lecturer = self.request.user
        return super(LectureCreateView, self).form_valid(form)
