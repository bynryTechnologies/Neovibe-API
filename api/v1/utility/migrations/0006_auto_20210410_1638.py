# Generated by Django 3.0.11 on 2021-04-10 11:08

from django.db import migrations, models
import v1.utility.models.utility_master


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0005_utilitymaster_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilitymaster',
            name='long_logo',
            field=models.FileField(blank=True, null=True, upload_to=v1.utility.models.utility_master.get_file_path),
        ),
        migrations.AlterField(
            model_name='utilitymaster',
            name='short_logo',
            field=models.FileField(blank=True, null=True, upload_to=v1.utility.models.utility_master.get_file_path),
        ),
    ]
