# Generated by Django 4.2.7 on 2024-08-17 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_alter_nin_talentprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
