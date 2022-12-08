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


class GradeSubmitForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['lecture', 'submission']
        widgets = {
            'lecture': forms.Select(attrs={'class': 'form-control'}),
            'submission': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GradeSubmitForm, self).__init__(*args, **kwargs)

    def clean(self):
        # check if already submitted
        if Grade.objects.filter(lecture=self.cleaned_data['lecture'], student=self.request.user).exists():
            raise forms.ValidationError("You have already submitted for this lecture")
        return self.cleaned_data