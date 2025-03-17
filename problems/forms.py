from problems.models import EcoProblem
from django import forms

class EcoProblemReportForm(forms.ModelForm):
    class Meta:
        model = EcoProblem
        fields = ['title', 'description', 'address', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
