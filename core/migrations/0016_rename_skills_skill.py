# Generated by Django 4.2.7 on 2024-06-07 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_talentprofile_digital_skills_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skills',
            new_name='Skill',
        ),
    ]
