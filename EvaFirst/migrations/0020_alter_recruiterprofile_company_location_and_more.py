# Generated by Django 4.2 on 2024-08-06 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EvaFirst', '0019_managerprofile_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiterprofile',
            name='company_location',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recruiterprofile',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recruiterprofile',
            name='recruiter_Firstname',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recruiterprofile',
            name='recruiter_Lastname',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recruiterprofile',
            name='recruiter_email',
            field=models.EmailField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recruiterprofile',
            name='recruiter_id_Num',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
