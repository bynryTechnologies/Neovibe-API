# Generated by Django 3.0.11 on 2021-03-18 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0003_auto_20210318_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilitypaymentchannel',
            name='utility_product_id',
        ),
    ]