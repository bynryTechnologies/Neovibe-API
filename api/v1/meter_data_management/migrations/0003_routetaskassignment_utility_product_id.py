# Generated by Django 3.0.3 on 2021-05-18 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_data_management', '0002_auto_20210424_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='routetaskassignment',
            name='utility_product_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
