# Generated by Django 3.0.3 on 2021-06-07 04:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0005_tenantstatus_short_name'),
        ('utility', '0006_auto_20210527_1849'),
        ('meter_data_management', '0007_schedulelog_schedule_log_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewConsumerDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('schedule_log_id', models.BigIntegerField(blank=True, null=True)),
                ('read_cycle_id', models.BigIntegerField(blank=True, null=True)),
                ('route_id', models.BigIntegerField(blank=True, null=True)),
                ('meter_reader_id', models.BigIntegerField(blank=True, null=True)),
                ('premise_id', models.BigIntegerField(blank=True, null=True)),
                ('activity_type_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('consumer_no', models.CharField(blank=True, max_length=200, null=True)),
                ('meter_no', models.CharField(blank=True, max_length=200, null=True)),
                ('current_meter_reading', models.CharField(blank=True, max_length=200, null=True)),
                ('meter_status_id', models.BigIntegerField(blank=True, null=True)),
                ('reader_status_id', models.BigIntegerField(blank=True, null=True)),
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
