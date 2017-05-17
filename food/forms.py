from django import forms
from .models import Food, FoodCategory

class FoodForm(forms.ModelForm):
    #定义一个元类，用来描述表单属性
    class Meta:
        model = Food
        # 用一个list结构来按照顺序排列表单字段名字，其中一些字段如商店名，创建时间等，默认自动添加，标签由于是外键，单独渲染
        fields = ['name', 'price', 'status']


class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ['name']

