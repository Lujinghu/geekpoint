# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0011_auto_20170417_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=models.IntegerField(verbose_name='订单号', null=True, unique_for_date='created_time'),
        ),
    ]
