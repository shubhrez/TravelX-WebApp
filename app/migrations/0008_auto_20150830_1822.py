# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150827_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('area', models.CharField(default=b'', max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('mpoly', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='place',
            name='location',
            field=models.ForeignKey(to='app.Location', null=True),
            preserve_default=True,
        ),
    ]
