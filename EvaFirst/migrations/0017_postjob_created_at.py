# Generated by Django 4.2 on 2024-08-05 21:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('EvaFirst', '0016_remove_applications_applyed_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postjob',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
