from django.db import models
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
        if user in self.shop_managers.all():
            return False
        self.shop_managers.add(user)
        return True

    def remove_manager(self, user):
        if user in self.shop_managers.all():
            return False
        self.shop_managers.remove(user)
        return True

    objects = ShopManager()
