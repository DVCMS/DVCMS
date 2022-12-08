from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView

from auth.roles import is_lecturer, is_student
from grades.forms import FilterLecturerForm, GradeCreateForm, GradeSubmitForm
from grades.models import Grade


@method_decorator(login_required, name='dispatch')
class GradeListView(ListView):
    model = Grade
    template_name = 'grades/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        if is_student(self.request.user):
            lecturer = self.request.GET.get("lecturer")
            if lecturer:
                return Grade.objects.raw(f"""
                    SELECT *
                    FROM   'grades_grade'
                           INNER JOIN 'auth_user'
                                   ON( 'grades_grade'. 'student_id' = 'auth_user'. 'id' )
                           INNER JOIN 'lectures_lecture'
                                   ON( 'grades_grade'. 'lecture_id' = 'lectures_lecture'. 'id' )
                           INNER JOIN 'auth_user' T4
                                   ON( 'lectures_lecture'. 'lecturer_id' = T4. 'id' )
                    WHERE ( 'auth_user'. 'username' = '{self.request.user.username}'
                            AND T4. 'username' LIKE '%{lecturer}%') 
                """)
            return Grade.objects.filter(student=self.request.user)
        elif is_lecturer(self.request.user):
            return Grade.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GradeListView, self).get_context_data(**kwargs)
        context['student'] = is_student(self.request.user)
        context['lecturer'] = is_lecturer(self.request.user)
        context['filter_lecturer'] = FilterLecturerForm
        context['filtered'] = self.request.GET.get("lecturer")
        return context


@method_decorator(login_required, name='dispatch')
class GradeUpdateView(UpdateView):
    model = Grade
    template_name = 'grades/grade_edit.html'
    success_url = reverse_lazy('grades:list')
    fields = ['grade', 'comment']

    def get(self, request, *args, **kwargs):
        if is_lecturer(self.request.user):
            self.fields = ['grade']
        elif is_student(self.request.user):
            self.fields = ['comment']
        return super(GradeUpdateView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_lecturer), name='dispatch')
class GradeCreateView(CreateView):
    model = Grade
    template_name = 'grades/grade_create.html'
    form_class = GradeCreateForm
    success_url = reverse_lazy('grades:list')

    def get_form_kwargs(self):
        kwargs = super(GradeCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_student), name='dispatch')
class GradeSubmitView(CreateView):
    model = Grade
    template_name = 'grades/grade_submit.html'
    form_class = GradeSubmitForm
    success_url = reverse_lazy('grades:list')

    def get_form_kwargs(self):
        kwargs = super(GradeSubmitView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super(GradeSubmitView, self).form_valid(form)
