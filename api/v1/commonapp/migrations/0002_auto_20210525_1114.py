# Generated by Django 3.0.11 on 2021-05-25 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subarea',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
