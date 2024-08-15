# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('manager', 'Manager'),
        ('recruiter', 'Recruiter'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES)

class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_profile',  editable=False)
    studentFirstname = models.CharField(default="", max_length=100)
    studentLastname = models.CharField(default="", max_length=100)
    student_mob = models.CharField(default="",max_length=12, blank=True, null=True)
    student_rollNo = models.CharField(default="",max_length=50, blank=True, null=True)
    student_address = models.TextField(blank=True, null=True)
    std_university  = models.CharField(default="", max_length=100, blank=True, null=True)
    std_college  = models.CharField(default="", max_length=100, blank=True, null=True)
    latest_edu  = models.CharField(default="",max_length=100, blank=True, null=True)
    passing_year= models.CharField(default="",max_length=80, blank=True, null=True)
    mark = models.CharField(default="",max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profilePic/', blank=True, null=True) 
    skills = models.CharField(default="",max_length=200, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # Add other student-specific fields
    def __str__(self) -> str:
        return (f"{self.studentFirstname} ")

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile', editable=False)
    manager_Firstname = models.CharField(default="", max_length=100, blank=True, null=True)
    manager_Lastname = models.CharField(default="", max_length=100, blank=True, null=True)
    manager_email = models.EmailField(max_length=100, blank=True, null=True)
    manager_mob = models.CharField(default="",max_length=12, blank=True, null=True)
    manager_dep  = models.CharField(default="",max_length=112, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    

    # Add other manager-specific fields
    def __str__(self) -> str:
        return (f"{self.manager_Firstname}")


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile', editable=False)
    recruiter_Firstname = models.CharField(default="", max_length=100, blank=True, null=True)
    recruiter_Lastname = models.CharField(default="", max_length=100, blank=True, null=True)
    recruiter_email = models.EmailField(default="", max_length=100,blank=True, null=True)
    recruiter_mob = models.CharField(default="",max_length=12, blank=True, null=True)
    recruiter_id_Num =  models.CharField(default="", max_length=100,blank=True, null=True)
    company_name =   models.CharField(default="", max_length=100, blank=True, null=True)
    about_comp =  models.TextField(default="", blank=True, null=True)
    company_location =  models.CharField(default="",max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # Add other recruiter-specific 
    def __str__(self) -> str:
        return (f"{self. recruiter_Firstname} ")
    

class omg(models.Model):
    name = models.CharField(default="", max_length=100)

class PostJob(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='post_job', editable=False)
    company_name = models.CharField(default="", max_length=100)
    job_title = models.CharField(default="", max_length=100)
    Sector= models.CharField(default="", max_length=100, blank=True, null=True)
    job_role = models.TextField(default="", blank=True, null=True)
    qualification = models.CharField(default="", max_length=100)
    experience = models.CharField(default="", max_length=100)
    about_job = models.TextField(default="", blank=True, null=True)
    location =models.CharField(default="", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.job_title
    

class Applications(models.Model):
    jobpostInfoFK = models.ForeignKey(PostJob, on_delete=models.CASCADE, related_name='post_job', editable=False)
    postId = models.IntegerField(default =0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Applicants_mob = models.CharField(max_length=100, default ="")
    Applicants_email = models.CharField(max_length=100, default ="")
    education = models.TextField()
    experience = models.TextField()
    resume = models.FileField(upload_to='media/resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
