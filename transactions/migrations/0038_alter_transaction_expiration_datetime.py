# Generated by Django 4.1.3 on 2022-11-19 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0037_alter_transaction_expiration_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 20, 16, 55, 26, 998444, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
