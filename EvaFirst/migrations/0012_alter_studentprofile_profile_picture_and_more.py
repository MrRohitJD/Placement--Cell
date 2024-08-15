# Generated by Django 4.2 on 2024-08-02 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EvaFirst', '0011_alter_studentprofile_mark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profilePic/'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]
