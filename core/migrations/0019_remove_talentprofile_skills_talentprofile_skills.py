# Generated by Django 4.2.7 on 2024-06-07 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_talentprofile_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talentprofile',
            name='skills',
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='skills',
            field=models.ManyToManyField(related_name='skills', to='core.skill'),
        ),
    ]
