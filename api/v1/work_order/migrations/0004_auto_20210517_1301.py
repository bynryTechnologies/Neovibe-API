# Generated by Django 3.0.3 on 2021-05-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0003_auto_20210503_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceappointment',
            name='cron_expression',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='serviceappointment',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='serviceappointment',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
