# Generated by Django 4.2.7 on 2024-09-10 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_remove_talentprofile_banned_user_banned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='banned',
            new_name='is_banned',
        ),
    ]
