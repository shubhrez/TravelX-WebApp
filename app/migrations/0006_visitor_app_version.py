# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_visitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='app_version',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
