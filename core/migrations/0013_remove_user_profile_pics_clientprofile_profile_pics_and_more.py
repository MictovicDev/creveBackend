# Generated by Django 4.2.7 on 2024-01-12 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_user_fullname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_pics',
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='profile_pics',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='files/images'),
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='profile_pics',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='files/images'),
        ),
    ]