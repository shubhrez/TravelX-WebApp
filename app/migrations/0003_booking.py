# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150914_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('date_of_booking', models.DateTimeField(null=True, blank=True)),
                ('place', models.ForeignKey(to='app.Place')),
                ('user', models.ForeignKey(to='app.UserProfile')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
