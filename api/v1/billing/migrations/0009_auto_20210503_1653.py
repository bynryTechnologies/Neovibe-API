# Generated by Django 3.0.3 on 2021-05-03 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_merge_20210425_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='qr_code',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
