# Generated by Django 4.2.7 on 2024-07-24 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_talentprofile_cover_image_and_more'),
        ('chat', '0003_message_reciever_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='reciever',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_chats', to='core.clientprofile'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_chats', to='core.talentprofile'),
        ),
    ]
