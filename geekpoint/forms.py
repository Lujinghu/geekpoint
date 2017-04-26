from django import forms
from . import models
from django.contrib.auth.models import User

class FoodForm(forms.ModelForm):
    #定义一个元类，用来描述表单属性
    class Meta:
        model = models.Food
        # 用一个list结构来按照顺序排列表单字段名字，其中一些字段如商店名，创建时间等，默认自动添加，标签由于是外键，单独渲染
        fields = ['name', 'price', 'status']


class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = models.FoodCategory
        fields = ['name']


class ShopForm(forms.ModelForm):
    class Meta:
        model = models.Shop
        fields = ['name', 'address', 'phone', 'cardAccount', 'table_nums', 'is_open']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='再次输入密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        #每个表单实例都会有个cleaned_data字典
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
