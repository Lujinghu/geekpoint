from django.db import models
from shop.models import Shop
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from food.models import Food


class OrderManagger(models.Manager):

    def query_by_user(self, user):
        return user.order_set.all().order_by('-created_time').filter(is_delete_by_consumer=False)

    def query_by_status(self, status, shop):
        return self.query_by_shop(shop).filter(status=status)

    def query_by_shop(self, shop):
        return shop.order_set.all().filter(is_delete_by_shop=False)

    def query_by_today(self, shop):
        return self.query_by_shop(shop).filter(
            created_time__day=timezone.now().day
        ).filter(created_time__month=timezone.now().month).filter(created_time__year=timezone.now().year)
    #上面的查询语句使用是没有问题的，但是要先安装一个叫做pytz的模块，这个模块可以正确的处理时间信息

class Order(models.Model):
    ORDER_STATUS = (
        ('x', '已下单'),
        ('q', '已确认'),
        ('f', '已付款'),
    )

    order_no = models.CharField('订单号', unique=True, null=True, max_length=256)
    table_no = models.CharField('桌号', max_length=200, null=True)
    total = models.FloatField('总价', default=0)
    shop = models.ForeignKey(Shop, verbose_name='商店', on_delete=models.SET_NULL, null=True) #定义一个订单与商店的一对多关系
    consumer = models.ForeignKey(User, default=None, verbose_name='顾客')
    foods = models.ManyToManyField(Food, verbose_name='菜品', through='OrderFood')
    is_delete_by_consumer = models.BooleanField(default=False)
    is_delete_by_shop = models.BooleanField(default=False)
    status = models.CharField('状态', max_length=1, choices=ORDER_STATUS, default='x')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '订单: %s' % self.order_no

    def get_absolute_url(self):
        return reverse('geekpoint:get_order', args=[str(self.id)])

    objects = OrderManagger()

    def check_consumer(self, user):
        return self.consumer == user#注意：不能用is关键字

    def delete_by_consumer(self):
        self.is_delete_by_consumer = True
        self.save()

    def delete_by_shop(self):
        self.is_delete_by_shop = True
        self.save()

    def change_status(self, status):
        self.status = status
        self.save()


#中间表，用来查询食物数量
class OrderFood(models.Model):
    food = models.ForeignKey(Food)
    order = models.ForeignKey(Order)
    nums = models.PositiveIntegerField(default=1)