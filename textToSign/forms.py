from django import forms
from .models import *
class SignToTextForm(forms.ModelForm):
    class Meta:
        model = SignToTextImage
        fields = ('image',)