# Generated by Django 3.0.11 on 2021-06-10 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_data_management', '0008_newconsumerdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newconsumerdetail',
            name='consumer_no',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='newconsumerdetail',
            name='meter_no',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
