# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Uploaded image'),
        ),
    ]
