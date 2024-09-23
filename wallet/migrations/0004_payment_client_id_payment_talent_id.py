# Generated by Django 4.2.7 on 2024-09-20 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_bookedcreative_status'),
        ('wallet', '0003_remove_payment_crypto_remove_payment_local_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='client_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.clientprofile'),
        ),
        migrations.AddField(
            model_name='payment',
            name='talent_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.talentprofile'),
        ),
    ]
