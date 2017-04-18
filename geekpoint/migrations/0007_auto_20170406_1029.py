# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0006_auto_20170406_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='shop',
            field=models.ForeignKey(to='geekpoint.Shop', verbose_name='商店'),
        ),
    ]
