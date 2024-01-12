# Generated by Django 4.2.7 on 2024-01-12 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_clientprofile_current_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientprofile',
            name='profile_pics',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='profile_pics',
        ),
        migrations.RemoveField(
            model_name='user',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lastname',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pics',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='files/images'),
        ),
        migrations.AlterField(
            model_name='clientprofile',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]