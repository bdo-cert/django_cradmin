# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-05 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cradmin_gettingstarted', '0004_auto_20170228_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='number_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]