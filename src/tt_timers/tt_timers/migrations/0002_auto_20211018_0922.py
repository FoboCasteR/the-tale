# Generated by Django 3.0.11 on 2021-10-18 09:22

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tt_timers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
