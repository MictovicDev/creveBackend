# Generated by Django 4.2.7 on 2024-07-31 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_talentprofile_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientprofile',
            name='profile_pics',
            field=models.ImageField(blank=True, default='files/images/newdefault.png', null=True, upload_to='files/images'),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='profile_pics',
            field=models.ImageField(blank=True, default='newdefault.png', null=True, upload_to='files/images'),
        ),
    ]
