# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-03-10 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightcurve', '0008_lightcurve_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='lightcurvereduction',
            name='target_color_index',
            field=models.FloatField(null=True),
        ),
    ]
