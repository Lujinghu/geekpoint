# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0014_auto_20170421_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='category',
        ),
        migrations.RemoveField(
            model_name='food',
            name='shop',
        ),
        migrations.RemoveField(
            model_name='foodcategory',
            name='shop',
        ),
        migrations.RemoveField(
            model_name='order',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='foods',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shop',
        ),
        migrations.RemoveField(
            model_name='orderfood',
            name='food',
        ),
        migrations.RemoveField(
            model_name='orderfood',
            name='order',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='shop_managers',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.DeleteModel(
            name='FoodCategory',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderFood',
        ),
        migrations.DeleteModel(
            name='Shop',
        ),
    ]
