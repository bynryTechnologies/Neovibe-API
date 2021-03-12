# Generated by Django 3.0.3 on 2021-03-10 09:08

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20210310_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='registration_obj',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
        ),
        migrations.AlterField(
            model_name='registration',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 605309), null=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 605309), null=True),
        ),
        migrations.AlterField(
            model_name='registrationstatus',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 606334), null=True),
        ),
        migrations.AlterField(
            model_name='registrationstatus',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 606334), null=True),
        ),
        migrations.AlterField(
            model_name='registrationsubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 603341), null=True),
        ),
        migrations.AlterField(
            model_name='registrationsubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 603341), null=True),
        ),
        migrations.AlterField(
            model_name='registrationtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 602346), null=True),
        ),
        migrations.AlterField(
            model_name='registrationtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 10, 14, 38, 40, 602346), null=True),
        ),
    ]
