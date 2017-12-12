# Generated by Django 2.0 on 2017-12-12 03:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MasterExpenseCategoryMain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MasterExpenseCategorySub',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('masterExpenseCategoryMain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MasterExpenseCategoryMain')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MasterIncomeCategoryMain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MasterIncomeCategorySub',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('masterIncomeCategoryMain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MasterIncomeCategoryMain')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionExpense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('expenseDate', models.DateField()),
                ('amount', models.BigIntegerField()),
                ('paymentRecipientName', models.CharField(blank=True, default='', max_length=30)),
                ('note', models.TextField()),
                ('masterExpenseCategorySub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MasterExpenseCategorySub')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionIncome',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('incomeDate', models.DateField()),
                ('amount', models.BigIntegerField()),
                ('paymentSourceName', models.CharField(blank=True, default='', max_length=30)),
                ('note', models.TextField()),
                ('masterIncomeCategorySub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.MasterIncomeCategorySub')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
