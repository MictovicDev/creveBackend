# Generated by Django 4.2.7 on 2024-08-19 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_remove_verification_user_verification_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to='core.talentprofile'),
        ),
    ]
