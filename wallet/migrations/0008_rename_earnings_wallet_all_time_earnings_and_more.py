# Generated by Django 4.2.7 on 2024-10-01 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0007_payment_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='earnings',
            new_name='all_time_earnings',
        ),
        migrations.AlterField(
            model_name='wallet',
            name='pin',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='AllTimeEarnings',
        ),
    ]
