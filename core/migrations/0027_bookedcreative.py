# Generated by Django 4.2.7 on 2024-06-15 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_remove_user_phone_number_talentprofile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedCreative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('client_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.clientprofile')),
                ('talent_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.talentprofile')),
            ],
        ),
    ]
