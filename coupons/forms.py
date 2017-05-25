from django import forms
from .models import DisCountCoupon

class CouponApplyForm(forms.Form):
    code = forms.CharField()


class CouponCreateForm(forms.ModelForm):
    class Meta:
        model = DisCountCoupon