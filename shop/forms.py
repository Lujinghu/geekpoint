from django import forms
from .models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'phone', 'cardAccount', 'table_nums', 'is_open']


class AddShopManagerForm(forms.Form):
    email = forms.EmailField(label='电子邮件')