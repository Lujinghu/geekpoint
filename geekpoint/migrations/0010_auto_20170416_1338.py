# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekpoint', '0009_auto_20170414_1359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='Category',
            new_name='category',
        ),
    ]
