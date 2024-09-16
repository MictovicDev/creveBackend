# Generated by Django 4.2.7 on 2024-09-12 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_rename_location_talentprofile_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='city',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='country',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='state',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
