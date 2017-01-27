# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-27 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cradmin_javascript_demos', '0004_fictionalfigure_is_godlike'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fictionalfigure',
            options={'ordering': ['sort_index', 'name']},
        ),
        migrations.AddField(
            model_name='fictionalfigure',
            name='sort_index',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]
