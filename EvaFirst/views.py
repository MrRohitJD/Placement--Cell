

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.models import User
from .models import StudentProfile, ManagerProfile, RecruiterProfile, PostJob, Applications
from .decorators import role_required
from django.contrib import messages
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    post = PostJob.objects.all()
    user = request.user.id
    print(post)
    userType = '/'
    profile_picture_url = 'https://th.bing.com/th/id/OIP.wRtvON_8JKRQghdROw5QvQHaHa?rs=1&pid=ImgDetMain' 
    if request.user.is_authenticated:
        logUser = request.user.role
        if logUser == 'student':
            userType = '/studentProfile/'
        elif logUser == 'manager':
            userType = '/managerProfile/'

        elif logUser == 'recruiter':
            userType ='/recruiterProfile/'

        context = {'logUserType': userType, 'profile_picture_url' :profile_picture_url , 'post' : post}
        if  request.method == 'POST':
            try:
                job_postid = request.POST.get('job_post')
                print(job_postid)
                job_post = PostJob.objects.get(id=job_postid)
                std =StudentProfile.objects.get(user_id=user)
                alpInfo  = Applications(
                    jobpostInfoFK = job_post,
                    first_name = std.studentFirstname,
                    last_name = std.studentLastname,
                    education = std.latest_edu,
                    experience = '00',
                    resume = std.resume,
                    Applicants_mob = std.student_mob,
                    Applicants_email = request.user.email
                )
                alpInfo.save()
                return render(request, 'success.html')
            except:
                messages.info(request, " Please! Login As Student" )
                return render(request, 'error.html')
        return render(request, 'home.html', context)
    # -----------------------Job posts-------------------------------  
    
    return render(request, 'home.html',  {'post' : post})

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        try:
            user = User.objects.create_user(first_name=username,username=email, email= email, password=password, role=role)
            messages.success(request, "User registered successfully please login " )
        except:
            messages.error(request, "User already exist please login with same credentials " )
            redirect('register') 
        finally:
            pass

            subject = "Welcome to Eva Placement Cell! Registration Successful"
            from_email  = ""
            text_content = ""
            to = email
            html_content = f"<p><strong>Dear {username},</strong></p><p>We are excited to inform you that your registration on Eva Placement Cell has been successfully completed. Below are your login details:</p><p><strong>Username:</strong> {username}<br><strong>Password:</strong> {password}</p><p>You can now log in using these credentials and start exploring all the features and services we offer. If you have any questions or need assistance, please do not hesitate to reach out to our support team.</p><p>For security reasons, we recommend changing your password after your first login.</p><p>Thank you for joining us!</p>"
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
        
        return redirect('login')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.role == 'student':
                messages.success(request, f"Student {user.first_name} Login successfully..." )
                return redirect('studentProfile')
            
            elif user.role == 'manager':
                messages.success(request, f"Manager {user.first_name} Login successfully..." )
                return redirect('managerProfile')
            elif user.role == 'recruiter':
                messages.success(request, f"Recruiter {user.first_name} Login successfully..." )
                return redirect('recruiterProfile')
            else:
                messages.error(request, "User Not Login " )
                return redirect('login')  # Default redirect if no role matches
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout(request):
    if auth_logout(request):
        return HttpResponseRedirect('/') # Redirect to home page or any other page
    return HttpResponseRedirect('/')



@role_required('student')
def studentProfile(request):

    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        surname = request.POST.get('surname')
        mobileNumber = request.POST.get('mobileNumber')
        address = request.POST.get('address')
        university = request.POST.get('university')
        college = request.POST.get('college')
        course = request.POST.get('course')
        passingYear = request.POST.get('passingYear')
        rollNum = request.POST.get('rollNum')
        marks = request.POST.get('marks')
        skills = request.POST.get('skills')
        resume = request.FILES.get('resume')  # Corrected: Use get() instead of ()
        profileimg = request.FILES.get('profileimg')  # Corrected: Use get() instead of ()
        print(resume)
        print(profileimg)
        userr = request.user
        try:
            profile = StudentProfile.objects.get(user=userr)
            if firstName != "":
                profile.studentFirstname = firstName
            if surname != "":
                profile.studentLastname = surname
            if mobileNumber != "":
                profile.student_mob = mobileNumber
            if rollNum != "":
                profile.student_rollNo = rollNum
            if address != "":
                profile.student_address = address
            if university != "":
                profile.std_university = university
            if college != "":
                profile.std_college = college
            if course != "":
                profile.latest_edu = course
            if marks != "":
                profile.mark = marks
            if passingYear != "": 
                profile.passing_year = passingYear
            if skills != "":
                profile.skills = skills

            if resume  and resume!= None:
                profile.resume = resume  # Only update if a new resume is provided
                
            if profileimg and profileimg!= None:
                profile.profile_picture = profileimg  # Only update if a new resume is provided
            messages.success(request, "Updated Your Profile" )

        except StudentProfile.DoesNotExist:
            profile = StudentProfile(
                user=userr,
                studentFirstname=firstName,
                studentLastname=surname,
                student_mob=mobileNumber,
                student_rollNo=rollNum,
                student_address=address,
                std_university=university,
                std_college=college,
                latest_edu=course,
                mark=marks,
                passing_year=passingYear,
                skills=skills,
                resume=resume,
                profile_picture = profileimg
            )
            messages.info(request, "Successfully added User Information" )

        profile.save()
        return redirect('studentProfile')
    
    existstd = request.user
    try:
        student_info =""
        student_info = StudentProfile.objects.get(user=existstd)
        print(student_info,"dddddddddd")
        
    except:pass
    userType = '/'
    logUser = request.user.role
        
    if logUser == 'student':
            userType = '/studentProfile/'

    elif logUser == 'manager':
            userType = '/managerProfile/'

    elif logUser == 'recruiter':
            userType ='/recruiterProfile/'

    context = {'logUserType': userType, "student_info" : student_info}
    return render(request, 'stdProf.html', context)

@role_required('manager')
def managerProfile(request):
    user = request.user
    
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        surname = request.POST.get('surname')
        mobileNumber = request.POST.get('mobileNumber')
        emailId = request.POST.get('emailId')
        department =  request.POST.get('department')
        try:
            profile = ManagerProfile.objects.get(user=user)
            if firstName !="" :
                profile.manager_Firstname = firstName
            if surname !="" :
                profile.manager_Lastname = surname
            if emailId !="" :
                profile.manager_email = emailId
            if mobileNumber !="" :
                profile.manager_mob = mobileNumber
            if department!="" :
                profile.manager_dep = department
            profile.save()
            messages.success(request, "Updated Your Profile" )
        except ManagerProfile.DoesNotExist:
            Mprofile = ManagerProfile.objects.create(
                user=user,
                manager_Firstname=firstName,
                manager_Lastname=surname,
                manager_mob=mobileNumber,
                manager_email = emailId,
                manager_dep = department

            )
            messages.info(request, "Successfully added User Information" )
            return redirect('managerProfile')
    try:
        if ManagerProfile.objects.filter(user=user).exists():
            profile = ManagerProfile.objects.get(user=user)
            context ={'profile' : profile}
            return render(request, 'managerPro.html', context )
    except:pass
    return render(request, 'managerPro.html' )


@role_required('recruiter')
def recruiterProfile(request):
    user = request.user
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'form_one':
            Company = request.POST.get('CompanyName')
            jobtitle = request.POST.get('jobtitle')
            SectorR = request.POST.get('Sector')
            aboutComp = request.POST.get('aboutComp')
            qualification = request.POST.get('qualification')
            experience = request.POST.get('experience')
            Loc = request.POST.get('loc')
            about_Job = request.POST.get('about_Job')

            try:
                recruiter_profile =RecruiterProfile.objects.get(user=user)

                post_job = PostJob(
                recruiter=recruiter_profile,
                company_name=Company,
                job_title=jobtitle,
                Sector = SectorR,
                job_role=aboutComp,
                qualification=qualification,
                experience=experience,
                location = Loc,
                about_job=about_Job
                )
                post_job.save()
                messages.success(request, "job Posted Successfully..." )
            except:
                messages.error(request, "Please First Complete your Profile" )
            return redirect('recruiterProfile')

        elif form_type == 'form_two':
            firstName = request.POST.get('firstName')
            surname = request.POST.get('surname')
            mobileNumber = request.POST.get('mobileNumber')
            emailId = request.POST.get('emailId')
            CompanyName =  request.POST.get('CompanyName')
            compid =  request.POST.get('compid')
            comp_about =  request.POST.get('comp_about')
            address =  request.POST.get('address')
            
            try:
                profile = RecruiterProfile.objects.get(user=user)
                if firstName !="":
                    profile.recruiter_Firstname = firstName
                if surname !="":
                    profile.recruiter_Lastname = surname
                if emailId !="":
                    profile.recruiter_email = emailId
                if mobileNumber !="":
                    profile.recruiter_mob = mobileNumber
                if CompanyName !="":
                    profile.company_name = CompanyName
                if compid !="":
                    profile.recruiter_id_Num = compid
                if comp_about !="":
                    profile.about_comp = comp_about
                if address !="":
                    profile.company_location = address
                messages.success(request, "Updated Your Profile" )
                profile.save()
            except RecruiterProfile.DoesNotExist:
                profile = RecruiterProfile.objects.create(
                    user=user,
                    recruiter_Firstname=firstName,
                    recruiter_Lastname=surname,
                    recruiter_mob=mobileNumber,
                    recruiter_email = emailId,
                    company_name = CompanyName,
                    recruiter_id_Num = compid,
                    about_comp = comp_about,
                    company_location = address
                )
                messages.info(request, "Successfully added User Information" )
            return redirect('recruiterProfile')
    try:
        if RecruiterProfile.objects.filter(user=user).exists():
            profile = RecruiterProfile.objects.get(user=user)
            context ={'profile' : profile}
            return render(request, 'recruProf.html', context )
    except:pass
        
    return render(request, 'recruProf.html' )



@role_required('manager')
def studentInfo(request):
    userType = '/'
    logUser = request.user.role
    student = StudentProfile.objects.all()
    if logUser == 'student':
        userType = '/studentProfile/'

    elif logUser == 'manager':
        userType = '/managerProfile/'

    elif logUser == 'recruiter':
        userType ='/recruiterProfile/'

    context = {'student': student, 'userType' : userType}
    return render(request, 'std_Info.html', context)


@role_required('manager')
def recruiterInfo(request):
    recruiter = RecruiterProfile.objects.all();
    userType = '/'
    logUser = request.user.role
    student = StudentProfile.objects.all()
    if logUser == 'student':
        userType = '/studentProfile/'

    elif logUser == 'manager':
        userType = '/managerProfile/'

    elif logUser == 'recruiter':
        userType ='/recruiterProfile/'

    context = {'recruiter' : recruiter, 'userType' : userType}
    return render(request, 'rec_Info.html', context)



def joblist(request):

    user = request.user.id
    post = None
    total_jobs = None
    try:
        pass
    except StudentProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student profile not found'})
    
    if  request.method == 'POST':
        try:
            job_postid = request.POST.get('job_post')
            print(job_postid)
            job_post = PostJob.objects.get(id=job_postid)
            job_post_ids = request.POST.getlist('job_posts[]')
            print(job_post_ids)
            std =StudentProfile.objects.get(user_id=user)
            alpInfo  = Applications(
                jobpostInfoFK = job_post,
                first_name = std.studentFirstname,
                last_name = std.studentLastname,
                education = std.latest_edu,
                experience = '00',
                resume = std.resume,
                Applicants_mob = std.student_mob,
                Applicants_email = request.user.email
            )
            alpInfo.save()
            return render(request, 'success.html')
        except:
            return render(request, 'error.html')
    else:
            userType = '/'
            
            if request.user.is_authenticated:
                logUser = request.user.role
                if logUser == 'student':
                    userType = 'studentProfile'

                elif logUser == 'manager':
                    userType = 'managerProfile'

                elif logUser == 'recruiter':
                    userType ='recruiterProfile'
            sector = request.GET.get('sector')
            print(sector, "hhhhhhhhhhhhhhhhhhhhhhh")
            if sector:
                post = PostJob.objects.filter(Sector=sector)
                print(post, "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
            elif post is None:
                post = PostJob.objects.all()
                total_jobs = PostJob.objects.count()

                context = {'post' : post, 'logUserType': userType, 'total_jobs' : total_jobs}
                return render(request, 'jobList.html', context)
            context = {'post' : post, 'logUserType': userType}
            return render(request, 'jobList.html', context)

@role_required('manager')
def showApplications(request):
    userType = '/'
    logUser = request.user.role
    email_list_str =None
    ApplicationsInfo = None
    if request.method== "POST":
        form_type = request.POST.get('form_type')
        if form_type =="sendMail":
            Subject = request.POST.get('Subject')
            emailList = request.POST.get('emailList')
            content = request.POST.get('mytextarea')
            email_list1 = [email.strip() for email in emailList.split(',')]
            subject = str(Subject)
            print(subject)
            print(type(subject))
            from_email  = ""
            text_content = ""
            to = email_list1
            html_content = content
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
                messages.success(request, "Mail Send successfully" )
            except:
                messages.error(request, "Mail service is under maintenance" )

        elif form_type =="removeH":
            application_ids = request.POST.getlist('application_ids[]')
            try:
                if application_ids:
                    Applications.objects.filter(id__in = application_ids).delete()
                    messages.success(request, "Application deleted" )
            except:
                messages.error(request, "Some error occurred!" )
        
    elif request.method == "GET":
        
        form_type = request.GET.get('form_type')
        if form_type == "searchForm":
            
            search_postID = request.GET.get('searchpostID')
            print(search_postID)
            search_aplID = request.GET.get('search_aplID')
            search_fname = request.GET.get('searchfname')
            print(search_fname)
            search_lname = request.GET.get('searchlname')
            search_mob_no = request.GET.get('searchmob_no')
            search_emailin = request.GET.get('searchemailin')
            search_education = request.GET.get('searcheducation')
            print(search_education)
            search_exp = request.GET.get('searchexp')
            
            
            
            query = Applications.objects.all()
            if search_postID:
                print(search_postID)
                query = query.filter(jobpostInfoFK_id=search_postID)
                print(Applications.objects.values_list('jobpostInfoFK'))
                # print(query)
            if search_aplID:
                query = query.filter(id=search_aplID)
                
            if search_fname:
                query = query.filter(first_name=search_fname)
            if search_lname:
                query = query.filter(last_name=search_lname)
            if search_mob_no:
                query = query.filter(Applicants_mob=search_mob_no)
            if search_emailin:
                query = query.filter(Applicants_email=search_emailin)
            if search_education:
                query = query.filter(education=search_education)
            if search_exp:
                query = query.filter(experience=search_exp)
            ApplicationsInfo = query
            
            email_listQ = ApplicationsInfo.values_list('Applicants_email', flat=True)
            email_list = list(email_listQ)
            email_list_str = ', '.join(email_list)
            
    if ApplicationsInfo is None:
            email_listQ = Applications.objects.values_list('Applicants_email', flat=True)
            email_list = list(email_listQ)
            email_list_str = ', '.join(email_list)
            ApplicationsInfo = Applications.objects.all()
            
    if logUser == 'student':
            userType = '/studentProfile/'

    elif logUser == 'manager':
            userType = '/managerProfile/'

    elif logUser == 'recruiter':
            userType ='/recruiterProfile/'


    context = {
        'ApplicationsInfo': ApplicationsInfo,
        'email_list_str': email_list_str,
        'userType' : userType
    }

    return render(request, 'applyInfo.html', context)

@login_required
def success(request):
    return render(request, 'success.html')


def about(request):
    userType = logtype(request)
    return render(request, 'about.html', {'userType' : userType})


def jobdetails(request, id):
    jobId = PostJob.objects.get(id = id)
    postID = PostJob.objects.all()
    user = request.user.id
    try:
        if request.method == 'POST':
                job_postid = request.POST.get('job_post')
                job_post = PostJob.objects.get(id=id)
                std =StudentProfile.objects.get(user_id=user)
                alpInfo  = Applications(
                    jobpostInfoFK = job_post,
                    first_name = std.studentFirstname,
                    last_name = std.studentLastname,
                    education = std.latest_edu,
                    experience = '00',
                    resume = std.resume,
                    Applicants_mob = std.student_mob,
                    Applicants_email = request.user.email
                )
                alpInfo.save()
                return render(request, 'success.html')
    except:
        return render(request, 'error.html')
    context = {'jobId':jobId, 'postID' :postID}
    return render(request,"jobdetails.html", context)


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
            subject = "Password Reset Request"
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, "An email has been sent with instructions to reset your password." )
            return redirect('password_reset')
        except User.DoesNotExist:
            return HttpResponse("This email is not registered.")
    return render(request, 'registration/password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            return HttpResponse("<h4>Password has been reset successfully. Click <a href='/login/'> here</a> to Login </h4>")
        return render(request, 'registration/password_reset_confirm.html', {'user': user})
    else:
        return HttpResponse("The reset link is invalid.")


@role_required('student')
def studentApplyJob(request):
    user = request.user
    logUser = user.role
    applied_jobs = Applications.objects.filter(Applicants_email=user.email).select_related('jobpostInfoFK')
    print(applied_jobs, "llllllllllllllllllllllllllllll")
    job_post_ids = applied_jobs.values_list('jobpostInfoFK_id', flat=True)
    posts = PostJob.objects.filter(id__in=job_post_ids)
    print(posts)
    a="lll"
    if logUser == 'student':
        userType = '/studentProfile/'

    elif logUser == 'manager':
        userType = '/managerProfile/'

    elif logUser == 'recruiter':
        userType ='/recruiterProfile/'

    userStd = StudentProfile.objects.get(user= user)
    context = {'applyJobs': posts, 'student_info' : userStd, 'userType': userType}
    return render(request , 'stdApplyJobs.html', context)

@role_required('recruiter')
def recPostedjobs(request):
    user = request.user
    print(user.id)
    currRecui = RecruiterProfile.objects.get(user=user.id)
    recruiter_profile_id = currRecui.id
    print(recruiter_profile_id)

    if request.method =="POST":
        delPOSTjob = request.POST.get('deletePost')
        PostJob.objects.get(id=delPOSTjob).delete()

    recuipostJob = PostJob.objects.filter(recruiter= recruiter_profile_id)
    print(recuipostJob)
    context = {'recuipostJob' :recuipostJob}
    return render(request , 'recruPostJobs.html', context)

    

def logtype(request):
    if request.user.is_authenticated:
        logUser = request.user.role
        if logUser == 'student':
            return '/studentProfile/'
        elif logUser == 'manager':
            return '/managerProfile/'
        elif logUser == 'recruiter':
            return '/recruiterProfile/'
    return ""


def nav(request):
    userType = '/'
    logUser = request.user.role
        
    if logUser == 'student':
        userType = 'studentProfile'

    elif logUser == 'manager':
        userType = 'managerProfile'

    elif logUser == 'recruiter':
        userType ='recruiterProfile'

    return render(request,'custom_widgets/ProfileNav.html', {'userType' : userType}  )



