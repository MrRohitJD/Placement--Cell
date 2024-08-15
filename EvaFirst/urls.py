"""
URL configuration for Eva project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .views import password_reset_request, password_reset_confirm

from .import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.home, name='home' ),
    path('register/', views.register, name='register'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('studentProfile/', views.studentProfile,name='studentProfile'),
    path('studentProfile/applyed_jobs/', views.studentApplyJob,name='studentApplyJob'),
    path('managerProfile/', views.managerProfile,name='managerProfile'),
    path('recruiterProfile/', views.recruiterProfile,name='recruiterProfile'),
    path('recruiterProfile/postedjobs/', views.recPostedjobs,name='postedjobs'),
    path('joblist/', views.joblist, name= 'joblist' ),
    path('managerProfile/std_info/', views.studentInfo, name='studentInfo'),
    path('managerProfile/rec_info/', views.recruiterInfo, name='recruiterInfo'),
    path('managerProfile/applications/', views.showApplications, name='showApplications'),
    path('success/' , views.success , name='success'),
    path('about/' , views.about , name='about'),
    path('about.html', RedirectView.as_view(url='/static/about.html', permanent=False)),
    path('jobdetails/<id>', views.jobdetails, name='jobdetails'),

    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)