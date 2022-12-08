from django import forms

from grades.models import Grade


class FilterLecturerForm(forms.Form):
    lecturer = forms.CharField(label="Filter By Lecturer", required=False)

class GradeCreateForm(forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        super(GradeCreateForm, self).__init__(*args, **kwargs)
        self.fields['lecture'].queryset = self.fields['lecture'].queryset.filter(lecturer=request.user)

    class Meta:
        model = Grade
        fields = ['lecture', 'grade', 'student']
        widgets = {
            'lecture': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }