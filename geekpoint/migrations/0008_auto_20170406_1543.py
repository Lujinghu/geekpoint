# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0007_auto_20170406_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table_no',
            field=models.CharField(max_length=200, null=True, verbose_name='桌号'),
        ),
    ]
