from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class ShopManager(models.Manager):

    def query_by_user(self, user):
        return user.shop_set.all()


class Shop(models.Model):
    name = models.CharField('商店名', max_length=50)
    address = models.CharField('地址', max_length=100)
    phone = models.CharField('电话', max_length=20)
    cardAccount = models.CharField('收款账号', max_length=30)
    table_nums = models.IntegerField('桌子数', default=0)
    is_open = models.BooleanField('正在营业',default=True)
    shop_managers = models.ManyToManyField(User, blank=True, verbose_name='管理员')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def check_manager(self, user):
        shop_manager_list = self.shop_managers.all()
        return user in shop_manager_list

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('geekpoint:charge_shop', args=[str(self.id)])

    def add_manager(self, user):
        self.shop_managers.add(user)

    objects = ShopManager()



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
    foods = models.ManyToManyField('Food', verbose_name='菜品', through='OrderFood')
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

    def query_by_order(self, order_id):
        order = Order.objects.get(id=order_id)
        return order.foods.all()

    def query_by_shop(self, shop):
        return shop.food_set.all()

class Food(models.Model):

    FOOD_STATUS = (
        ('z', '有库存'),
        ('q', '售罄'),
    )

    name = models.CharField('食物名', max_length=50)
    price = models.FloatField('价格')
    shop = models.ForeignKey(Shop, verbose_name='商店')  #食物与商铺是一对多的关系，定义外键foreignKey在多的一侧
    category = models.ForeignKey(FoodCategory, null=True, blank=True)
    status = models.CharField('食品状态', max_length=1, choices=FOOD_STATUS, default='z')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    '''
    def get_absolute_url(self):
        return reverse('geekpoint:charge_food')
    '''
    objects = FoodManager()#更改默认查询管理器

#中间表，用来查询食物数量
class OrderFood(models.Model):
    food = models.ForeignKey(Food)
    order = models.ForeignKey(Order)
    nums = models.PositiveIntegerField(default=1)

