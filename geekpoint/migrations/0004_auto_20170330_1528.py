# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geekpoint', '0003_auto_20170330_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='shop_manager',
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_manager',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='管理员', blank=True),
        ),
    ]
