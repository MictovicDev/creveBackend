# Generated by Django 4.2.7 on 2024-06-07 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_talentprofile_skills_talentprofile_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='skills',
            field=models.ManyToManyField(to='core.skill'),
        ),
    ]
