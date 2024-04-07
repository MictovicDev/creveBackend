# Generated by Django 4.2.7 on 2024-04-07 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_talentnotification_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentnotification',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='talentnotification', to='core.talentprofile'),
        ),
    ]
