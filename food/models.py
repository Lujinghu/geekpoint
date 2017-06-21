from django.db import models
from shop.models import Shop
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class FoodCategory(models.Model):
    name = models.CharField('标签名', max_length=50)
    shop = models.ForeignKey(Shop, verbose_name='商店')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True) #修改时间，每次保存时自动添加

    def __str__(self):
        return self.name


class FoodManager(models.Manager):

    def query_by_category(self, shop, foodcategory_id):
        return self.query_by_shop(shop).filter(category_id=foodcategory_id)

    def query_by_shop(self, shop):
        return shop.food_set.all()

class Food(models.Model):

    FOOD_STATUS = (
        ('z', '有库存'),
        ('q', '售罄'),
    )

    name = models.CharField('食物名', max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    shop = models.ForeignKey(Shop, verbose_name='商店')  #食物与商铺是一对多的关系，定义外键foreignKey在多的一侧
    category = models.ForeignKey(FoodCategory, null=True, blank=True)
    status = models.CharField('食品状态', max_length=1, choices=FOOD_STATUS, default='z')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return redirect(reverse('food:edit_food', args=[self.shop.id, self.id, ]))

    objects = FoodManager()#更改默认查询管理器



