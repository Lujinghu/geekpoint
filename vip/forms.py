from django import forms
from .models import Vip

class VipAddForm(forms.ModelForm):
    class Meta:
        model = Vip