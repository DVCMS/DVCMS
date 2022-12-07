from django import forms

from lectures.models import Lecture


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['name']

    def clean(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long')
        if Lecture.objects.filter(name=name).exists():
            raise forms.ValidationError('This lecture already exists!')
        return self.cleaned_data
