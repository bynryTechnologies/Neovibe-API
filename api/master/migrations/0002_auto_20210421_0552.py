# Generated by Django 3.0.3 on 2021-04-21 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masteruser',
            name='email',
            field=models.CharField(max_length=200),
        ),
    ]
