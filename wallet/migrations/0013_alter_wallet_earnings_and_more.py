# Generated by Django 4.2.7 on 2024-10-06 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0012_rename_client_id_solpayment_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='earnings',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='withdrawable_balance',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
