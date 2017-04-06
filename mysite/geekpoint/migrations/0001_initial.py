# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, verbose_name='食物名')),
                ('price', models.FloatField(verbose_name='价格')),
                ('status', models.CharField(verbose_name='食品状态', max_length=1, choices=[('z', '有库存'), ('q', '售罄')], default='z')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, verbose_name='标签名')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('order_no', models.IntegerField(unique_for_date='created_time', verbose_name='订单号')),
                ('table_no', models.CharField(max_length=200, verbose_name='桌号')),
                ('total', models.FloatField(verbose_name='总价')),
                ('foods', models.TextField(verbose_name='食物列表')),
                ('is_delete', models.BooleanField(default=False)),
                ('status', models.CharField(verbose_name='状态', max_length=1, choices=[('x', '已下单'), ('q', '已确认'), ('w', '已完成'), ('f', '已付款')], default='x')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('consumer', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, verbose_name='顾客')),
            ],
        ),
        migrations.CreateModel(
            name='OrderFood',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nums', models.PositiveIntegerField()),
                ('food', models.ForeignKey(to='geekpoint.Food')),
                ('order', models.ForeignKey(to='geekpoint.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('owner_id', models.IntegerField()),
                ('name', models.CharField(max_length=50, verbose_name='商店名')),
                ('address', models.CharField(max_length=100, verbose_name='地址')),
                ('phone', models.CharField(max_length=20, verbose_name='电话')),
                ('cardAccount', models.CharField(max_length=30, verbose_name='收款账号')),
                ('table_nums', models.IntegerField(default=0, verbose_name='桌子数')),
                ('is_open', models.BooleanField(default=True, verbose_name='正在营业')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(to='geekpoint.Shop', verbose_name='商店'),
        ),
        migrations.AddField(
            model_name='foodcategory',
            name='shop',
            field=models.ForeignKey(to='geekpoint.Shop', verbose_name='商店'),
        ),
        migrations.AddField(
            model_name='food',
            name='Category',
            field=models.ForeignKey(blank=True, to='geekpoint.FoodCategory', null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='shop',
            field=models.ForeignKey(to='geekpoint.Shop', verbose_name='商店'),
        ),
    ]
