# Generated by Django 4.2.7 on 2024-03-07 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_review_relevant_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='relevant_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
