# Generated by Django 3.0.7 on 2020-06-15 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0004_auto_20200615_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='can_validate_participant_a',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='can_validate_participant_b',
        ),
    ]
