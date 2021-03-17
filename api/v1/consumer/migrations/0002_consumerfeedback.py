# Generated by Django 3.0.11 on 2021-03-17 06:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0001_initial'),
        ('tenant', '0001_initial'),
        ('consumer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('consumer_id', models.BigIntegerField(blank=True, null=True)),
                ('feedback', models.CharField(blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
    ]