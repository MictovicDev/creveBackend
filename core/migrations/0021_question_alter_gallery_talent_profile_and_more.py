# Generated by Django 4.2.7 on 2024-01-18 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_skill_talent_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=500, null=True)),
                ('talent_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.talentprofile')),
            ],
        ),
        migrations.AlterField(
            model_name='gallery',
            name='talent_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='core.talentprofile'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='talent_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='core.talentprofile'),
        ),
        migrations.AlterField(
            model_name='worktype',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_type', to='core.talentprofile'),
        ),
        migrations.DeleteModel(
            name='Questions',
        ),
    ]
