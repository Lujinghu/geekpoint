from django.db import models
from shop.models import Shop
from django.contrib.auth.models import User

class Vip(models.Model):
    shop = models.ForeignKey(Shop, verbose_name='商店名')
    user = models.ForeignKey(User, verbose_name='会员名')
    consum_point = models.IntegerField('消费积分', default=0)
    active = models.BooleanField('是否有效', default=True)

    def add_consum_point(self, point):
        self.consum_point += point
        self.save()

    def shut_consum_point(self, point):
        self.consum_point -= point
        self.save()

    def deactive(self):
        self.active = False
        self.save()

    def active(self):
        self.active = True
        self.save()