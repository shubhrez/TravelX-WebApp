# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150731_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('heading', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Image',
            new_name='Gallery',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='link',
            new_name='image_link',
        ),
        migrations.AddField(
            model_name='place',
            name='description',
            field=models.ManyToManyField(default=None, to='app.Description'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='place',
            name='gallery',
            field=models.ManyToManyField(default=None, to='app.Gallery'),
            preserve_default=True,
        ),
    ]
