# Generated by Django 4.2.7 on 2024-09-20 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_crypto_local_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='crypto',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='local',
        ),
        migrations.AddField(
            model_name='payment',
            name='value',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Crypto',
        ),
        migrations.DeleteModel(
            name='Local',
        ),
    ]