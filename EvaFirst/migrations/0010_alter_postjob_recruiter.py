# Generated by Django 4.2 on 2024-08-02 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EvaFirst', '0009_alter_applications_applicants_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postjob',
            name='recruiter',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='post_job', to='EvaFirst.recruiterprofile'),
        ),
    ]
