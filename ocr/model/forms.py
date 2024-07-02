

from django import forms
from .models import CheckData

class CheckUploadForm(forms.ModelForm):
    class Meta:
        model = CheckData
        fields = ['bank_name', 'check_image']
