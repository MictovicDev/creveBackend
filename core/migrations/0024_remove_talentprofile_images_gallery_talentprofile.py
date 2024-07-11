# Generated by Django 4.2.7 on 2024-06-08 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_skill_talentprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talentprofile',
            name='images',
        ),
        migrations.AddField(
            model_name='gallery',
            name='talentprofile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.talentprofile'),
        ),
    ]
