# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
from django.contrib.gis.geos import Point


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagedmodel',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=Point(-104.9903, 39.7392, srid=4326)),
        ),
    ]
