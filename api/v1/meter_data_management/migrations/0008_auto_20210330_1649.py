# Generated by Django 3.0.11 on 2021-03-30 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_data_management', '0007_uploadroute'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='utility_product_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='readcycle',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
