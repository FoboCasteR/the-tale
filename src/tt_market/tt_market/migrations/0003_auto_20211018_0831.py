# Generated by Django 3.0.11 on 2021-10-18 08:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tt_market', '0002_auto_20190415_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logrecord',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
