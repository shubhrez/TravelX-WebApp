# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150803_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='description',
        ),
        migrations.AddField(
            model_name='description',
            name='place',
            field=models.ForeignKey(to='app.Place', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='place',
            name='duration',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
