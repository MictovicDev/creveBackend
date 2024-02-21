# Generated by Django 4.2.7 on 2024-01-22 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_workschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='workschedule',
            name='talent_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.talentprofile'),
        ),
        migrations.AlterField(
            model_name='workschedule',
            name='day',
            field=models.CharField(blank=True, choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=500, null=True),
        ),
    ]