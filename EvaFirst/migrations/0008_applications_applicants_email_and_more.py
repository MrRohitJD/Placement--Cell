# Generated by Django 4.2 on 2024-07-31 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EvaFirst', '0007_alter_applications_jobpostinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='Applicants_email',
            field=models.CharField(default='default_value', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applications',
            name='Applicants_mob',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
