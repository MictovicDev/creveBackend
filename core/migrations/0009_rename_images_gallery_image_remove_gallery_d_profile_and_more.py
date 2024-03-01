# Generated by Django 4.2.7 on 2024-02-28 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_skills_skill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='images',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='d_profile',
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='images',
            field=models.ManyToManyField(to='core.gallery'),
        ),
    ]
