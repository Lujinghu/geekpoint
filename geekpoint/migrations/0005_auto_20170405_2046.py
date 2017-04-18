# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0004_auto_20170330_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('x', '已下单'), ('q', '已确认'), ('f', '已付款')], max_length=1, default='x', verbose_name='状态'),
        ),
    ]
