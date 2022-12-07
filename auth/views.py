import hashlib

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import FormView

from auth.forms import AuthenticationForm, ForgotPasswordForm
from auth.models import SecurityQuestion


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('grades:list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, User.objects.get(username=form.user_cache[0].username))
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        return redirect('grades:list')


class ForgotPasswordView(FormView):
    template_name = 'auth/forgot_password.html'
    form_class = ForgotPasswordForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('grades:list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ForgotPasswordView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        if username:
            context['username'] = username
            security_question = SecurityQuestion.objects.filter(user__username=username)
            if len(security_question) > 0:
                context['question'] = security_question[0].question
            else:
                context['question'] = None
                context['error'] = "This user does not exist or have a secret answer set!"
        return context

    def get_form_kwargs(self):
        kwargs = super(ForgotPasswordView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = User.objects.get(username=self.request.GET.get("username"))
        user.password = hashlib.md5(form.cleaned_data.get('password1').encode()).hexdigest()
        user.save()
        login(self.request, user)
        return redirect('grades:list')
