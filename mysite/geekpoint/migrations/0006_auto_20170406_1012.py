# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0005_auto_20170405_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='shop',
            field=models.ForeignKey(to='geekpoint.Shop', verbose_name='商店', default=None),
        ),
    ]
