# Generated by Django 3.0.3 on 2021-03-31 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_bill_consumer_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='product_id',
            new_name='utility_product_id',
        ),
    ]