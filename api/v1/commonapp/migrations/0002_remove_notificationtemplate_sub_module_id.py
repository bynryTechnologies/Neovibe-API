# Generated by Django 3.0.3 on 2021-03-12 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationtemplate',
            name='sub_module_id',
        ),
    ]
