# Generated by Django 4.1.7 on 2023-03-12 08:44

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoanProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=256)),
                ('loan_limit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('duration', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('notification_channel', models.CharField(choices=[('SMS', 'SMS'), ('EMAIL', 'EMAIL'), ('ALL', 'ALL')], max_length=256)),
            ],
            options={
                'db_table': 'loan_product',
                'ordering': ['product_name'],
            },
        ),
    ]
