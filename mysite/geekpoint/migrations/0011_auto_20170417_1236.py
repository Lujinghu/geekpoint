# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geekpoint', '0010_auto_20170416_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='shop_manager',
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_managers',
            field=models.ManyToManyField(verbose_name='管理员', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
