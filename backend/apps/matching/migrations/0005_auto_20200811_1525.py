# Generated by Django 3.0.7 on 2020-08-11 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0004_auto_20200811_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['state', 'match_date']},
        ),
    ]
