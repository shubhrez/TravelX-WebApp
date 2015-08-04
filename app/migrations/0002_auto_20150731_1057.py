# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='description',
        ),
        migrations.RemoveField(
            model_name='place',
            name='images',
        ),
        migrations.AddField(
            model_name='place',
            name='category',
            field=models.ForeignKey(default=None, to='app.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='image',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='place',
            name='short_description',
            field=models.CharField(default=b'', max_length=300),
            preserve_default=True,
        ),
    ]
