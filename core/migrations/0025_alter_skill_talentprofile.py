# Generated by Django 4.2.7 on 2024-06-08 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_talentprofile_images_gallery_talentprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='talentprofile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dskills', to='core.talentprofile'),
        ),
    ]