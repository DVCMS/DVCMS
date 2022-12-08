from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

ROLE_CHOICES = (
    ('student', 'Student'),
    ('admin', 'Admin'),
    ('lecturer', 'Lecturer'),
)


class StudentForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'disabled':'disabled'}))

