# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-11 23:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cradmin_javascript_demos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FictionalFigureCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('primary_fictional_figure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='cradmin_javascript_demos.FictionalFigure')),
                ('promoted_fictional_figures', models.ManyToManyField(blank=True, to='cradmin_javascript_demos.FictionalFigure')),
                ('secondary_fictional_figure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='cradmin_javascript_demos.FictionalFigure')),
            ],
        ),
    ]
