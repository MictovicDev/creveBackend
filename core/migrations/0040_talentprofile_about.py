# Generated by Django 4.2.7 on 2024-02-22 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_alter_talentprofile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentprofile',
            name='about',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
