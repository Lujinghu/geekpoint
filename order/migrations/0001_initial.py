# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order_no', models.CharField(verbose_name='订单号', max_length=256, unique=True, null=True)),
                ('table_no', models.CharField(verbose_name='桌号', max_length=200, null=True)),
                ('total', models.FloatField(verbose_name='总价', default=0)),
                ('is_delete_by_consumer', models.BooleanField(default=False)),
                ('is_delete_by_shop', models.BooleanField(default=False)),
                ('status', models.CharField(verbose_name='状态', max_length=1, default='x', choices=[('x', '已下单'), ('q', '已确认'), ('f', '已付款')])),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('consumer', models.ForeignKey(verbose_name='顾客', default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderFood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nums', models.PositiveIntegerField(default=1)),
                ('food', models.ForeignKey(to='food.Food')),
                ('order', models.ForeignKey(to='order.Order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='foods',
            field=models.ManyToManyField(verbose_name='菜品', to='food.Food', through='order.OrderFood'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(verbose_name='商店', null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Shop'),
        ),
    ]
