# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('consum_point', models.IntegerField(verbose_name='消费积分', default=0)),
                ('shop', models.ForeignKey(verbose_name='商店名', to='shop.Shop')),
                ('user', models.ForeignKey(verbose_name='会员名', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
