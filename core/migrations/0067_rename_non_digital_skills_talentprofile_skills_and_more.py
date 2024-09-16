# Generated by Django 4.2.7 on 2024-09-15 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_rename_skills_talentprofile_non_digital_skills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talentprofile',
            old_name='non_digital_skills',
            new_name='skills',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='category',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='digital_skills',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='website_link',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='whatsapp_link',
        ),
    ]
