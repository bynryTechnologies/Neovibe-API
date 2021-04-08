# Generated by Django 3.0.3 on 2021-04-02 07:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0005_utilitymaster_user_id'),
        ('tenant', '0001_initial'),
        ('billing', '0005_auto_20210331_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedCharges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('meter_id', models.BigIntegerField(blank=True, null=True)),
                ('charges', models.BigIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
    ]