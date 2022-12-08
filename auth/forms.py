import hashlib

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from auth.models import SecurityQuestion


class AuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = User.objects.raw(
                f"SELECT * FROM auth_user WHERE username='{username}' AND password='{hashlib.md5(password.encode()).hexdigest()}'")
            if len(self.user_cache) == 0:
                raise self.get_invalid_login_error()
        return self.cleaned_data


class ForgotPasswordUsernameForm(forms.Form):
    username = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.question = None
        super().__init__(*args, **kwargs)

    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        if len(user) == 0:
            raise forms.ValidationError("Username does not exist")
        question = SecurityQuestion.objects.filter(user=user[0])
        if len(question) == 0:
            raise forms.ValidationError("Username does not have a security question")
        self.question = question[0]
        return self.cleaned_data


class ForgotPasswordForm(forms.Form):
    answer = forms.CharField(max_length=255)
    # two password fields
    password1 = forms.CharField(label="New Password", max_length=255, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", max_length=255, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        # Check if answer is correct
        question = SecurityQuestion.objects.get(user__username=self.request.GET.get("username"))
        if question.answer != self.cleaned_data.get('answer'):
            raise forms.ValidationError("Answer is incorrect")
        # Check if passwords match
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords do not match")

        return self.cleaned_data
