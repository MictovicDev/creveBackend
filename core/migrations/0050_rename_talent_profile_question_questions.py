# Generated by Django 4.2.7 on 2024-08-19 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_talentprofile_experience'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='talent_profile',
            new_name='questions',
        ),
    ]
