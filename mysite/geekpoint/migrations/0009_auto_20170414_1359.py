# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0008_auto_20170406_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_delete',
            new_name='is_delete_by_consumer',
        ),
        migrations.AddField(
            model_name='order',
            name='is_delete_by_shop',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='order',
            name='foods',
        ),
        migrations.AddField(
            model_name='order',
            name='foods',
            field=models.ManyToManyField(verbose_name='菜品', to='geekpoint.Food', through='geekpoint.OrderFood'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(verbose_name='总价', default=0),
        ),
        migrations.AlterField(
            model_name='orderfood',
            name='nums',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
