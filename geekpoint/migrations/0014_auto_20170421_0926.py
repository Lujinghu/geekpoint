# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0013_auto_20170417_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=models.CharField(verbose_name='订单号', max_length=256, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(verbose_name='商店', null=True, on_delete=django.db.models.deletion.SET_NULL, to='geekpoint.Shop'),
        ),
    ]
