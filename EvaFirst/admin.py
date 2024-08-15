from django.contrib import admin
from .models import  User, StudentProfile, ManagerProfile, RecruiterProfile, omg, PostJob , Applications

# # Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(ManagerProfile)
admin.site.register(RecruiterProfile)
admin.site.register(omg)
admin.site.register(PostJob)
admin.site.register(Applications)