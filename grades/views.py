from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from grades.forms import FilterLecturerForm
from grades.models import Grade


@method_decorator(login_required, name='dispatch')
class GradeListView(ListView):
    model = Grade
    template_name = 'grades/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GradeListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['filter_lecturer'] = FilterLecturerForm
        context['filtered'] = self.request.GET.get("lecturer")
        return context


@method_decorator(login_required, name='dispatch')
class GradeUpdateView(UpdateView):
    model = Grade
    template_name = 'grades/grade_edit.html'
    fields = ['comment']
    success_url = reverse_lazy('grades:list')

    def get_queryset(self):
        return Grade.objects.filter(student=self.request.user)
