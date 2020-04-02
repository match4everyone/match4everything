# Generated by Django 3.0.4 on 2020-04-02 17:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ineedstudent', '0003_merge_20200330_0124'),
        ('iamstudent', '0006_merge_20200330_0313'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='', max_length=200)),
                ('message', models.TextField(default='')),
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ineedstudent.Hospital')),
            ],
        ),
        migrations.AddField(
            model_name='emailtosend',
            name='email_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iamstudent.EmailGroup'),
        ),
    ]
