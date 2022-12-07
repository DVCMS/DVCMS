from django import forms

from grades.models import Grade


class FilterLecturerForm(forms.Form):
    lecturer = forms.CharField(label="Filter By Lecturer", required=False)
