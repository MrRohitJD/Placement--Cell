# Generated by Django 4.2 on 2024-08-08 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EvaFirst', '0021_postjob_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='applyStd_id',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
