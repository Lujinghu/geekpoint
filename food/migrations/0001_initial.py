# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='食物名', max_length=50)),
                ('price', models.FloatField(verbose_name='价格')),
                ('status', models.CharField(verbose_name='食品状态', max_length=1, default='z', choices=[('z', '有库存'), ('q', '售罄')])),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='标签名', max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(verbose_name='商店', to='shop.Shop')),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='category',
            field=models.ForeignKey(blank=True, null=True, to='food.FoodCategory'),
        ),
        migrations.AddField(
            model_name='food',
            name='shop',
            field=models.ForeignKey(verbose_name='商店', to='shop.Shop'),
        ),
    ]
