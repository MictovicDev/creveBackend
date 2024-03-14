# Generated by Django 4.2.7 on 2024-03-07 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_review_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reviewed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewed', to='core.talentprofile'),
        ),
    ]