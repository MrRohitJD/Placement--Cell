# Generated by Django 4.2 on 2024-08-05 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EvaFirst', '0014_applications_applyed_at_managerprofile_created_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='applyed_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='managerprofile',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='postjob',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='recruiterprofile',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
