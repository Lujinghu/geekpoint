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
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='商店名', max_length=50)),
                ('address', models.CharField(verbose_name='地址', max_length=100)),
                ('phone', models.CharField(verbose_name='电话', max_length=20)),
                ('cardAccount', models.CharField(verbose_name='收款账号', max_length=30)),
                ('table_nums', models.IntegerField(verbose_name='桌子数', default=0)),
                ('is_open', models.BooleanField(verbose_name='正在营业', default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('shop_managers', models.ManyToManyField(verbose_name='管理员', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
