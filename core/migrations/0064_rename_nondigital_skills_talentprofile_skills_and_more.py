# Generated by Django 4.2.7 on 2024-09-13 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_clientprofile_city_clientprofile_country_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talentprofile',
            old_name='nondigital_skills',
            new_name='skills',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='digital_skills',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='starting_price',
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
