# Generated by Django 3.0.11 on 2021-05-26 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0004_utilitymaster_document_generated_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilitymaster',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
