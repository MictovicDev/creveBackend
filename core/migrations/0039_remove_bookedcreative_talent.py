# Generated by Django 4.2.7 on 2024-07-11 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_bookedcreative_talent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookedcreative',
            name='talent',
        ),
    ]