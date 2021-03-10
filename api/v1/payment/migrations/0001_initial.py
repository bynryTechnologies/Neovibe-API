# Generated by Django 3.0.10 on 2021-03-10 16:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fsm.fsm
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utility', '__first__'),
        ('tenant', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('key', models.CharField(blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentSubType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('key', models.CharField(blank=True, max_length=200, null=True)),
                ('payment_type_id', models.BigIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('key', models.CharField(blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('identification_id', models.BigIntegerField(blank=True, null=True)),
                ('transaction_type_id', models.BigIntegerField(blank=True, null=True)),
                ('transaction_sub_type_id', models.BigIntegerField(blank=True, null=True)),
                ('transaction_amount', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('transaction_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'SETTLED')], default=0)),
                ('payment_id', models.BigIntegerField(blank=True, null=True)),
                ('settlement_amount', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('settlement_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_transaction_tenant', to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_transaction_utility', to='utility.UtilityMaster')),
            ],
            bases=(models.Model, fsm.fsm.FiniteStateMachineMixin),
        ),
        migrations.CreateModel(
            name='PaymentSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('consumer_no', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'APPROVED'), (2, 'REJECTED'), (3, 'PENDING')], default=0)),
                ('payment_type_id', models.BigIntegerField(blank=True, null=True)),
                ('identification_id', models.BigIntegerField(blank=True, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=200, null=True)),
                ('transaction_amount', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('transaction_charges', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('transaction_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('payment_mode_id', models.BigIntegerField(blank=True, null=True)),
                ('payment_channel_id', models.BigIntegerField(blank=True, null=True)),
                ('payment_source_id', models.BigIntegerField(blank=True, null=True)),
                ('receipt_no', models.CharField(blank=True, max_length=200, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=200, null=True)),
                ('account_no', models.CharField(blank=True, max_length=200, null=True)),
                ('cheque_dd_no', models.CharField(blank=True, max_length=200, null=True)),
                ('cheque_dd_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_penalty', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant', to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='utility', to='utility.UtilityMaster')),
            ],
            bases=(models.Model, fsm.fsm.FiniteStateMachineMixin),
        ),
    ]
