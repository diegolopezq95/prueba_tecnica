from django import forms
from .models import Senior


class SeniorForm(forms.ModelForm):
    greeting = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Senior
        fields = ['name', 'greeting', 'position']
