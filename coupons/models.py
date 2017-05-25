from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Shop

class DisCountCoupon(models.Model):
    code = models.CharField('优惠券码', max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()
    shop = models.ForeignKey(Shop)

    def __str__(self):
        return '优惠券：{}'.format(self.code)