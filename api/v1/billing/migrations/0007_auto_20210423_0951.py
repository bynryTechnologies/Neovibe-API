# Generated by Django 3.0.3 on 2021-04-23 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20210423_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='qr_code',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
