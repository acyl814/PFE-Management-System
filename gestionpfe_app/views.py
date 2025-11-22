

import logging
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.forms import FloatField
from django.shortcuts import get_object_or_404, render,redirect,reverse
from django.core.paginator import Paginator
from . import forms , models
from gestionpfe_app.forms import AdminForm
from django.db.models import Sum , Count , Q
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import time,timedelta,date
from django.conf import settings
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
import random
import datetime
from django.utils import timezone



def home_view (request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    return render(request,'gestionpfe/home-page.html' )

def contact_view(request):
    sub = forms.ContactForm()
    if request.method == 'POST':
        sub = forms.ContactForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['email']
            message = sub.cleaned_data['message']
            send_mail(email, message, settings.EMAIL_HOST_USER, [settings.EMAIL_RECEIVING_USER], fail_silently=False)
            return render(request, 'gestionpfe/contactsuccess.html')
    return render(request, 'gestionpfe/contact.html', {'form':sub})



def about_view (request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    return render(request, 'gestionpfe/about.html')

def login_choose_view (request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    return render(request, 'gestionpfe/login-choose.html')

def signup_choose_view (request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    return render(request, 'gestionpfe/signup-choose.html')

def signup_admin_view(request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    if request.method == 'POST':
        form = forms.SigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            admin = models.Admin.objects.create(user=user)
            my_admin_group, created = Group.objects.get_or_create(name='ADMIN')
            my_admin_group.user_set.add(user)
            return redirect('/login_admin/')
    else:
        form = forms.SigupForm()
    return render(request, 'gestionpfe/signup-admin.html', {'form': form})

def signup_teacher_view(request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    teacherForm = forms.TeacherForm()
    if request.method == 'POST':
        form = forms.SigupForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if form.is_valid() and teacherForm.is_valid():
            user = form.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.save()
            my_admin_group, created = Group.objects.get_or_create(name='TEACHER')
            my_admin_group.user_set.add(user)
            return redirect('/login_teacher/')
    else:
        form = forms.SigupForm()
        teacherForm = forms.TeacherForm()
    return render(request, 'gestionpfe/signup-ens.html', {'form':form,'teacherForm':teacherForm})


def signup_entreprise_view(request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    entrepriseForm = forms.EntrepriseForm()
    if request.method == 'POST':
        form = forms.SigupEntForm(request.POST)
        entrepriseForm=forms.EntrepriseForm(request.POST,request.FILES)
        if form.is_valid() and entrepriseForm.is_valid():
            user = form.save()
            ent = entrepriseForm.save(commit=False)
            ent.user = user
            ent.save()
            my_admin_group, created = Group.objects.get_or_create(name='ENTREPRISE')
            my_admin_group.user_set.add(user)
            return redirect('/login_entreprise/')
    else:
        form = forms.SigupEntForm()
        entrepriseForm = forms.EntrepriseForm()
    return render(request, 'gestionpfe/signup-ent.html', {'form':form,'entrepriseForm':entrepriseForm})


def signup_student_view(request):
    if request.user.is_authenticated:
        return redirect('/afterlogin')
    studentForm = forms.StudentForm()
    if request.method == 'POST':
        form = forms.SigupForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if form.is_valid() and studentForm.is_valid():
            user = form.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_admin_group, created = Group.objects.get_or_create(name='STUDENT')
            my_admin_group.user_set.add(user)
            return redirect('/login_student/')
    else:
        form = forms.SigupForm()
        studentForm = forms.StudentForm()
    return render(request, 'gestionpfe/signup-etd.html', {'form':form,'studentForm':studentForm})

#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_company(user):
    return user.groups.filter(name='ENTREPRISE').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def logout_view(request):
    logout(request)
    return redirect('/')


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        accountapproval = models.Admin.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            
            return redirect('/admin_dashboard')
        else:
            user = request.user.admin
            return render(request, 'gestionpfe/wait_for_approval.html',{'user':user})
    elif is_teacher(request.user):
        accountapproval = models.Teacher.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            teacher = request.user.teacher
            if not teacher.keyword:
                return redirect('/teacher_add_keyword')
            else:
                return redirect('/teacher_subject')
        else:
            user = request.user.teacher
            return render(request, 'gestionpfe/wait_for_approval.html',{'user':user})
    elif is_company(request.user):
        accountapproval = models.Enterprise.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('/teacher_subject')
        else:
            user = request.user.enterprise
            return render(request, 'gestionpfe/wait_for_approval.html',{'user':user})
    elif is_student(request.user):
        accountapproval = models.Student.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            user_student = request.user.student
            try:
                
                subject_choice = models.SubjectChoice.objects.get(Q(student=user_student.binome)|Q(student=user_student), validated_by_student=True) 
                if subject_choice:
                    return redirect('student_subject_details')
            except models.SubjectChoice.DoesNotExist:
                    return redirect('/student_view_subject')
        else:
            user = request.user.student
            return render(request, 'gestionpfe/wait_for_approval.html',{'user':user})
    else:
        return redirect('/admin')  
 
    
@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    
    
    admin=models.Admin.objects.all().filter(user = request.user.id)
    
    entreprises=models.Enterprise.objects.all().count()
    pendingentreprises=models.Enterprise.objects.all().filter(status=False).count()


    teachers=models.Teacher.objects.all().count()
    pendingteachers=models.Teacher.objects.all().filter(status=False).count()

    students=models.Student.objects.all().count()
    pendingstudents=models.Student.objects.all().filter(status=False).count()
    masterstudent = models.Student.objects.all().filter(level='2nd year master\'s degree').count()
    licencestudent = models.Student.objects.all().filter(level='3rd year bachelor\'s degree').count()

    subjects=models.Subject.objects.all().count()
    pendingsubjects=models.Subject.objects.all().filter(status='PENDING').count()
    
    departments=models.Department.objects.all().count()
    
    specialitys=models.Speciality.objects.all().count()
   
    


    return render(request,'gestionpfe/admin_dashboard.html', {'admin':admin , 'entreprises': entreprises, 
        'pendingentreprises':pendingentreprises,
        'teachers': teachers , 'pendingteachers' : pendingteachers ,'students':students,'pendingstudents':pendingstudents
        , 'masterstudent':masterstudent,'licencestudent': licencestudent , 'subjects':subjects, 
        'pendingsubjects':pendingsubjects, 'departments':departments, 
        'specialitys':specialitys

    })

#################################################################################################################

@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def admin_admin_view(request):
    admin=models.Admin.objects.all().filter(user = request.user.id)
    admins = models.Admin.objects.all().count()
    admins_active = models.Admin.objects.all().filter(status=True).count()
    
    # Fetch all admins excluding the currently logged-in admin.
    ent = models.Admin.objects.exclude(user=request.user)
    
    # Apply search filters if provided.
    search_term = request.GET.get('search_term', '')
    if search_term:
        ent = ent.filter(
            Q(user__username__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term)
        )

    admin_status = request.GET.get('admin_status', '')
    if admin_status == 'True':
        ent = ent.filter(status=True)
    elif admin_status == 'False':
        ent = ent.filter(status=False)
    else :
        ent=ent

    # Set up pagination.
    paginator = Paginator(ent, 7)  # 7 admins per page for example.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the admin list page.
    return render(request, 'gestionpfe/admin_users.html', {
        'admins': admins,
        'admins_active': admins_active,
        'page_obj': page_obj,
        'search_term': search_term,
        'admin_status': admin_status,'admin':admin
    })


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def approve_admin_view(request,pk):
    ent=models.Admin.objects.get(id=pk)
    ent.status=True
    ent.save()
    return redirect('admin_users')

@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def update_admin_view(request, pk):
    admin=models.Admin.objects.filter(user = request.user.id)
    
    ent = models.Admin.objects.get(id=pk)
    user = models.User.objects.get(id=ent.user_id)

    userForm = forms.SigupForm(instance=user, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
    })
    entForm = forms.AdminForm(instance=ent, initial={
        'status': ent.status,
    })
    userForm1 = forms.Sigup1Form(request.POST, instance=user)

    if request.method == 'POST':
        userForm = forms.SigupForm(request.POST, instance=user)
        userForm1 = forms.Sigup1Form(request.POST, instance=user)
        entForm = forms.AdminForm(request.POST, instance=ent)
        if entForm.is_valid():
            ent = entForm.save(commit=False)
            if userForm.has_changed():
                if userForm.is_valid():
                    user = userForm.save()
                    ent.user = user
            ent.status = True
            ent.save()
            return redirect('admin_users')
    
    return render(request, 'gestionpfe/admin_update_admin.html', {'userForm': userForm,'userForm1': userForm1, 'admin':admin,'entForm':entForm, 'ent':ent})



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def add_admin_view(request):
    admin=models.Admin.objects.all().filter(user = request.user.id)
    userForm = forms.SigupForm(request.POST)
    if request.method == 'POST':
        userForm = forms.SigupForm(request.POST)
        entForm=forms.AdminForm(request.POST)
        if userForm.is_valid() and entForm.is_valid():
            user=userForm.save()
            user.save()
            ent=entForm.save(commit=False)
            ent.user = user
            ent.status = True
            ent.save()
            my_admin_group, created = Group.objects.get_or_create(name='ADMIN')
            my_admin_group.user_set.add(user)
            return redirect('admin_users')
    else:
        userForm = forms.SigupForm()
        
    return render(request, 'gestionpfe/admin_add_admin.html', {'userForm':userForm,'admin':admin})


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def delete_admin_view(request,pk):
    ent=models.Admin.objects.get(id=pk)
    user=models.User.objects.get(id=ent.user_id)
    user.delete()
    ent.delete()
    return redirect('admin_users')
#################################################################################################################
@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def admin_entreprise_view(request):
    admin = models.Admin.objects.all().filter(user=request.user.id)
    entreprise = models.Enterprise.objects.all().count()
    entreprises_active = models.Enterprise.objects.filter(status=True).count()
    search_term = request.GET.get('search_term', '')
    entreprise_status = request.GET.get('entreprise_status', '')  # New filter parameter for status

    # Base query for all enterprises
    entreprises = models.Enterprise.objects.all()

    # Apply search filters if provided.
    if search_term:
        entreprises = entreprises.filter(
            Q(name__icontains=search_term) |
            Q(user__username__icontains=search_term)  # Assuming enterprises have an 'email' attribute
        )

    # Filter by status if specified
    if entreprise_status == 'True':
        entreprises = entreprises.filter(status=True)
    elif entreprise_status == 'False':
        entreprises = entreprises.filter(status=False)

    # Pagination
    paginator = Paginator(entreprises, 7)  # Adjust number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for the template
    context = {
        'entreprises': entreprise,
        'entreprises_active': entreprises_active,
        'page_obj': page_obj,
        'search_term': search_term,
        'entreprise_status': entreprise_status,
        'admin': admin
    }

    return render(request, 'gestionpfe/admin_entreprise.html', context)



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def approve_entreprise_view(request,pk):
    ent=models.Enterprise.objects.get(id=pk)
    ent.status=True
    ent.save()
    return redirect('admin_entreprise')

@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def update_entreprise_view(request, pk):
    admin = models.Admin.objects.all().filter(user=request.user.id)
    ent = models.Enterprise.objects.get(id=pk)
    user = models.User.objects.get(id=ent.user_id)

    userForm = forms.SigupEnt1Form(instance=user, initial={
        'username': user.username,
        'email': user.email,
    })
    entForm = forms.EntrepriseForm(instance=ent, initial={
        'name': ent.name,
        'status': ent.status,
    })

    if request.method == 'POST':
        userForm = forms.SigupEnt1Form(request.POST, instance=user)
        entForm = forms.EntrepriseForm(request.POST, instance=ent)
        if entForm.is_valid():
            ent = entForm.save(commit=False)
            if userForm.has_changed():
                if userForm.is_valid():
                    user = userForm.save()
                    ent.user = user
            ent.save()
            return redirect('admin_entreprise')
    
    return render(request, 'gestionpfe/admin_update_entreprise.html', {'userForm': userForm, 'entForm': entForm,'admin': admin})



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def add_entreprise_view(request):
    admin = models.Admin.objects.all().filter(user=request.user.id)
    entForm = forms.EntrepriseForm()
    userForm = forms.SigupEntForm(request.POST)
    if request.method == 'POST':
        userForm = forms.SigupEntForm(request.POST)
        entForm=forms.EntrepriseForm(request.POST)
        if userForm.is_valid() and entForm.is_valid():
            user=userForm.save()
            user.save()
            ent=entForm.save(commit=False)
            ent.user = user
            ent.status=True
            ent.save()
            my_admin_group, created = Group.objects.get_or_create(name='ENTREPRISE')
            my_admin_group.user_set.add(user)
            return redirect('admin_entreprise')
    else:
        userForm = forms.SigupEntForm()
        entForm = forms.EntrepriseForm()
    return render(request, 'gestionpfe/admin_add_entreprise.html', {'userForm':userForm,'entForm':entForm,'admin': admin})


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def delete_entreprise_view(request,pk):
    ent=models.Enterprise.objects.get(id=pk)
    user=models.User.objects.get(id=ent.user_id)
    user.delete()
    ent.delete()
    return redirect('admin_entreprise')

##########################################################################################
@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def admin_department_view(request):
    admin = models.Admin.objects.all().filter(user=request.user.id)
    search_term = request.GET.get('search_term', '')

    departments = models.Department.objects.all()  # Start with all departments
    department = departments.count()
   

    if search_term:
        departments = departments.filter(
            Q(name__icontains=search_term) |  # Search by department name
            Q(speciality__name__icontains=search_term)  # Assuming speciality is a related field
        )

    paginator = Paginator(departments, 7)  # Paginate the results, 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestionpfe/admin_department.html', {
        'page_obj': page_obj,
        'admin': admin,
        'search_term': search_term,
        'departments': department,
        
    })



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def add_department_view(request):
    admin = models.Admin.objects.filter(user=request.user)
    if request.method == 'POST':
        depForm = forms.DepartmentAddForm(request.POST)
        if depForm.is_valid():
            depForm.save()
            return redirect('admin_department')
    else:
        depForm = forms.DepartmentAddForm()
   
    return render(request, 'gestionpfe/admin_add_department.html', {'admin': admin,'depForm': depForm })

@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def delete_department_view(request,pk):
    dep=models.Department.objects.get(id=pk)
    dep.delete()
    return redirect('admin_department')


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def update_department_view(request, pk):
    admin = models.Admin.objects.filter(user=request.user)
    dep = models.Department.objects.get(id=pk)
    
    if request.method == 'POST':
        depForm = forms.DepartmentForm(request.POST, instance=dep, department_id=pk)
        if depForm.is_valid():
            depForm.save()
            return redirect('admin_department')
    else:
        # No need to set initial as it is already an instance form
        depForm = forms.DepartmentForm(instance=dep, department_id=pk)
    
    return render(request, 'gestionpfe/admin_update_department.html', {
        'admin': admin,
        'depForm': depForm
    })

################################################################################################
@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def admin_speciality_view(request):
    # Get the admin details for the sidebar links
    admin = models.Admin.objects.filter(user=request.user)

    # Fetch all specialities or filter them by search term
    search_term = request.GET.get('search_term', '')
    specialities = models.Speciality.objects.all()
    if search_term:
        specialities = specialities.filter(Q(name__icontains=search_term) | Q(department__name__icontains=search_term))

    # Pagination: Split specialities into pages
    paginator = Paginator(specialities, 7)  # 10 specialities per page, adjust as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Total specialities (used in the template for the total count display)
    total_specialities = models.Speciality.objects.all().count()

    # Render the page with the specialities list
    return render(request, 'gestionpfe/admin_speciality.html', {
        'page_obj': page_obj,
        'search_term': search_term,
        'specialitys': total_specialities,
        'admin': admin
    })


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def add_speciality_view(request):
    admin = models.Admin.objects.filter(user=request.user)
    speForm = forms.SpecialityForm()
    if request.method == 'POST':
        speForm = forms.SpecialityForm(request.POST)
        if speForm.is_valid():
            speForm.save()
            return redirect('admin_speciality')
    else:
        speForm = forms.SpecialityForm()
   
    return render(request, 'gestionpfe/admin_add_speciality.html',{'speForm': speForm,'admin': admin })
   
@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def delete_speciality_view(request,pk):
    spe=models.Speciality.objects.get(id=pk)
    spe.delete()
    return redirect('admin_speciality')


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def update_speciality_view(request, pk):
    spe = models.Speciality.objects.get(id=pk)
    speForm = forms.SpecialityForm(instance=spe, initial={
        'name': spe.name,
        'department': spe.department,
    })

    if request.method == 'POST':
        
        speForm = forms.SpecialityForm(request.POST, instance=spe)
        if speForm.is_valid():
            spe = speForm.save()
            return redirect('admin_speciality')
    
    return render(request, 'gestionpfe/admin_update_speciality.html',{'speForm': speForm })

##############################################################################


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    admin = models.Admin.objects.all().filter(user=request.user.id)
    teacher = models.Teacher.objects.all().count()
    teachers_active = models.Teacher.objects.filter(status=True).count()
    
    search_term = request.GET.get('search_term', '')
    teacher_status = request.GET.get('teacher_status', '')

    # Base query for all teachers
    teachers = models.Teacher.objects.select_related('user').all().order_by('user__last_name', 'user__first_name')

    # Filter by username, first name, last name, or department if search term is present
    if search_term:
        teachers = teachers.filter(
            Q(user__username__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(belongs__name__icontains=search_term)  # Assuming 'belongs' has a 'name' attribute
        )

    # Filter by status if specified
    if teacher_status == 'True':
        teachers = teachers.filter(status=True)
    elif teacher_status == 'False':
        teachers = teachers.filter(status=False)

    # Pagination
    paginator = Paginator(teachers, 7)  # Adjust the number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for the template
    context = {
        'teachers': teacher,
        'teachers_active': teachers_active,
        'page_obj': page_obj,
        'search_term': search_term,
        'teacher_status': teacher_status,
        'admin': admin
    }

    return render(request, 'gestionpfe/admin_teacher.html', context)


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    ent=models.Teacher.objects.get(id=pk)
    ent.status=True
    ent.save()
    return redirect('admin_teacher')



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def update_teacher_view(request, pk):
    admin=models.Admin.objects.filter(user = request.user.id)
    ent = models.Teacher.objects.get(id=pk)
    user = models.User.objects.get(id=ent.user_id)

    userForm = forms.Sigup1Form(instance=user)
    entForm = forms.TeacherForm(instance=ent, initial={
        'belongs': ent.belongs,
        'status': ent.status,
        
    })

    if request.method == 'POST':
        userForm = forms.Sigup1Form(request.POST, instance=user)
        entForm = forms.TeacherForm(request.POST, instance=ent)
        if entForm.is_valid():
            ent = entForm.save(commit=False)
            if userForm.has_changed():
                if userForm.is_valid():
                    user = userForm.save()
                    ent.user = user
            ent.save()
            return redirect('admin_teacher')
    
    return render(request, 'gestionpfe/admin_update_teacher.html', {'userForm': userForm, 'entForm': entForm, 'admin':admin})



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def add_teacher_view(request):
    admin=models.Admin.objects.filter(user = request.user.id)
    entForm = forms.TeacherForm()
    userForm = forms.SigupForm(request.POST)
    if request.method == 'POST':
        userForm = forms.SigupForm(request.POST)
        entForm=forms.TeacherForm(request.POST)
        if userForm.is_valid() and entForm.is_valid():
            user=userForm.save()
            user.save()
            ent=entForm.save(commit=False)
            ent.user = user
            ent.status= True
            ent.save()
            my_admin_group, created = Group.objects.get_or_create(name='TEACHER')
            my_admin_group.user_set.add(user)
            return redirect('admin_teacher')
    else:
        userForm = forms.SigupForm()
        entForm = forms.TeacherForm()
    return render(request, 'gestionpfe/admin_add_teacher.html', {'userForm':userForm,'entForm':entForm, 'admin':admin})


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    ent=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=ent.user_id)
    user.delete()
    ent.delete()
    return redirect('admin_teacher')

##########################################################################################

@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def admin_student_view(request):
    admin=models.Admin.objects.all().filter(user = request.user.id)
    student = models.Student.objects.all().count()
    students_active = models.Student.objects.all().filter(status=True).count()
    
    search_term = request.GET.get('search_term', '')
    level_filter = request.GET.get('level', '')  # Ajout du paramètre de niveau
   

    # Requête de base pour tous les étudiants
    students = models.Student.objects.all()

    # Filtrage par nom d'utilisateur, prénom ou nom de famille si le terme de recherche est présent
    if search_term:
        students = students.filter(
            Q(user__username__icontains=search_term) |
            Q(matricule__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(speciality__name__icontains=search_term)  # Assurez-vous que `speciality` a un attribut `name`
        )

    # Filtrage par niveau si spécifié
    if level_filter == 'True':
        students = students.filter(status=True)
    elif level_filter == 'False':
        students = students.filter(status=False)
    elif level_filter :
        students = students.filter(level=level_filter)

    # Pagination
    paginator = Paginator(students, 7)  # Modifier le nombre selon vos besoins
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexte pour le template
    context = {
        'students':student,
        'students_active':students_active,
        'page_obj': page_obj,
        'search_term': search_term,
        'level_filter': level_filter,
        'admin':admin
        
    }

    return render(request, 'gestionpfe/admin_student.html', context)




@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    ent=models.Student.objects.get(id=pk)
    ent.status=True
    ent.save()
    return redirect('admin_student')



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def update_student_view(request, pk):
    
    admin=models.Admin.objects.all().filter(user = request.user.id)
    ent = models.Student.objects.get(id=pk)
    user = models.User.objects.get(id=ent.user_id)

    userForm = forms.Sigup1Form(instance=user)
    entForm = forms.StudentForm(instance=ent, initial={
        'speciality': ent.speciality,
        'status': ent.status,
        'level': ent.level,
    })

    if request.method == 'POST':
        userForm = forms.Sigup1Form(request.POST)
        entForm = forms.StudentForm(request.POST, instance=ent)
        if entForm.is_valid():
            ent = entForm.save(commit=False)
            if userForm.has_changed():
                if userForm.is_valid():
                    user = userForm.save()
                    ent.user = user
            ent.save()
            return redirect('admin_student')
    
    return render(request, 'gestionpfe/admin_update_student.html', {'userForm': userForm, 'entForm': entForm, 'admin':admin})



@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def add_student_view(request):
    admin=models.Admin.objects.all().filter(user = request.user.id)
    entForm = forms.StudentForm()
    userForm = forms.SigupForm(request.POST)
    if request.method == 'POST':
        userForm = forms.SigupForm(request.POST)
        entForm=forms.StudentForm(request.POST)
        if userForm.is_valid() and entForm.is_valid():
            user=userForm.save()
            user.save()
            ent=entForm.save(commit=False)
            ent.user = user
            ent.status =True
            ent.save()
            my_admin_group, created = Group.objects.get_or_create(name='STUDENT')
            my_admin_group.user_set.add(user)
            return redirect('admin_student')
    else:
        userForm = forms.SigupForm()
        entForm = forms.StudentForm()
    return render(request, 'gestionpfe/admin_add_student.html', {'userForm':userForm,'entForm':entForm, 'admin':admin})


@login_required(login_url='login_admin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    ent=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=ent.user_id)
    user.delete()
    ent.delete()
    return redirect('admin_student')

#################################################################################################################

@login_required
@user_passes_test(lambda u: is_admin(u) or is_teacher(u))
def admin_subject_view(request):
    if is_admin(request.user):
        admin = models.Admin.objects.filter(user=request.user)
        subjects = models.Subject.objects.all()
        total_subjects = models.Subject.objects.count()
        pending_subjects = models.Subject.objects.filter(status='PENDING').count()

    if is_teacher(request.user):
        admin = models.Teacher.objects.filter(user=request.user)
        teacher = request.user.teacher
        
        # Exclude subjects created by the teacher
        commission_subject_ids = models.Subject.objects.filter(validation_commission=teacher).values_list('id', flat=True)
        approved_subject_ids = models.SubjectInteraction.objects.filter(
            teacher=teacher,
            action='approved'
        ).values_list('subject_id', flat=True)
        # Filtrer les sujets selon les conditions
        subjects = models.Subject.objects.filter(
            Q(status='PENDING') & Q(id__in=commission_subject_ids)
        ).exclude(id__in=approved_subject_ids)
        
    search_term = request.GET.get('search_term', '')
    filter_value = request.GET.get('filter', '')

    if search_term:
        subjects = subjects.filter(title__icontains=search_term)

    if filter_value:
        if filter_value in ['L3', 'M2']:
            subjects = subjects.filter(level=filter_value)
        elif filter_value in ['PENDING', 'APPROVED', 'REJECTED'] and is_admin(request.user):
            subjects = subjects.filter(status=filter_value)
        elif filter_value in ['External', 'Internal']:
            subjects = subjects.filter(type=filter_value)
        elif filter_value == " " and is_admin(request.user):
            subjects = models.Subject.objects.all()

    paginator = Paginator(subjects, 7)  # 10 subjects per page, adjust as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_term': search_term,
        'filter': filter_value,
        'admin': admin,
    }

    if is_admin(request.user):
        context['total_subjects'] = total_subjects
        context['pending_subjects'] = pending_subjects

    return render(request, 'gestionpfe/admin_subject.html', context)

@login_required
@user_passes_test(is_teacher)
def approve_subject_view(request, pk):
    subject = models.Subject.objects.get(id=pk)
    teacher = request.user.teacher

    # Vérifier si l'enseignant fait partie de la commission
    if teacher not in subject.validation_commission.all():
        return redirect('admin_subject')

    interaction, created = models.SubjectInteraction.objects.get_or_create(
        subject=subject,
        teacher=teacher,
        defaults={'action': 'approved'}
    )
    if not created:
        return redirect('admin_subject')

    # Vérifier les actions des membres de la commission
    interactions = models.SubjectInteraction.objects.filter(subject=subject)
    if interactions.filter(action='rejected').exists():
        subject.status = 'REJECTED'
    elif interactions.filter(action='approved').count() == 2:
        subject.status = 'APPROVED'
        subject.rejection_reason = ''
    subject.save()

    return redirect('admin_subject')
    

@login_required
@user_passes_test(lambda u: is_admin(u) or is_teacher(u))
def view_subject_view(request, pk):
    if is_admin:
        admin = models.Admin.objects.filter(user=request.user)
    if is_teacher :
        admin = models.Teacher.objects.filter(user=request.user)
    subject = models.Subject.objects.get(id=pk)
    form = forms.SubjectviewForm(instance=subject , initial= {
        'speciality':subject.speciality.get_name,
    })

    return render(request, 'gestionpfe/admin_view_subject.html', { 'admin': admin,'form': form})       


@login_required
@user_passes_test(is_teacher)
def reject_subject_view(request, pk):
    subject = models.Subject.objects.get(id=pk)
    teacher = request.user.teacher

    # Vérifier si l'enseignant fait partie de la commission
    if teacher not in subject.validation_commission.all():
        return redirect('admin_subject')

    if request.method == 'POST':
        form = forms.RejectSubjectForm(request.POST, instance=subject)
        if form.is_valid():
            rejection_reason = form.cleaned_data['rejection_reason']
            
            # Créer ou mettre à jour l'interaction de rejet
            interaction, created = models.SubjectInteraction.objects.get_or_create(
                subject=subject,
                teacher=teacher,
                defaults={'action': 'rejected'}
            )

            # Mettre à jour le sujet avec la raison de rejet
            subject.rejection_reason = rejection_reason
            subject.status = 'REJECTED'
            
            # Mise à jour du statut du sujet
            interactions = models.SubjectInteraction.objects.filter(subject=subject)

            if interactions.filter(action='approved').count() == 2:
                subject.status = 'APPROVED'
                subject.rejection_reason = ''  # Effacer les raisons de rejet en cas d'approbation

            subject.save()
            return redirect('admin_subject')
    else:
        form = forms.RejectSubjectForm(instance=subject)

    admin = models.Teacher.objects.filter(user=request.user)
    return render(request, 'gestionpfe/admin_reject_subject.html', {'admin': admin, 'form': form})


@login_required(login_url='/login_admin')
@user_passes_test(is_admin)
def admin_view_validated_choices(request):
    admin = models.Admin.objects.filter(user=request.user)
    search_term = request.GET.get('search_term', '')
    filter_value = request.GET.get('filter', '')
    defense_session_master = models.DefenseSession.objects.filter(level='2nd year master\'s degree').count()
    defense_session_licence = models.DefenseSession.objects.filter(level='3rd year bachelor\'s degree').count()

    # Base queryset
    validated_choices_qs = models.SubjectChoice.objects.filter(validated_by_student=True).select_related('subject', 'student')
    validated_choices_qs1 = models.SubjectChoice.objects.filter(validated_by_student=True).select_related('subject', 'student').count()
    # Search filter
    if search_term:
        validated_choices_qs = validated_choices_qs.filter(
            Q(student__user__first_name__icontains=search_term) |
            Q(student__user__last_name__icontains=search_term) |
            Q(subject__title__icontains=search_term)
        )

    # Level or Type filter
    if filter_value in ['L3', 'M2']:
        validated_choices_qs = validated_choices_qs.filter(student__level=filter_value)
    elif filter_value in ['External', 'Internal']:
        validated_choices_qs = validated_choices_qs.filter(subject__type=filter_value)

    paginator = Paginator(validated_choices_qs, 7)  # 10 subjects per page, adjust as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Pass the validated_choices queryset to the context
    context = {
        'admin': admin,
        'page_obj': page_obj,
        'total_choices': validated_choices_qs1,
        'filter': filter_value,
        'search_term': search_term,
        'defense_session_master':defense_session_master,
        'defense_session_licence':defense_session_licence
    }

    return render(request, 'gestionpfe/admin_validated_choices.html', context)

@login_required(login_url='/login_admin')
@user_passes_test(is_admin)
def admin_view_summary(request,pk):
    admin = models.Admin.objects.filter(user=request.user)
    choice = models.SubjectChoice.objects.get(id=pk)
    summary = models.Suivi.objects.filter(choice__subject__id = choice.subject.id)
    paginator = Paginator(summary, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'admin': admin,
        'page_obj': page_obj
    }

    return render(request, 'gestionpfe/admin_view_summary.html', context)


@login_required(login_url='/login_admin')
@user_passes_test(is_admin)
def create_defense_session(request):
    admin = models.Admin.objects.filter(user=request.user)
    if request.method == 'POST':
        form = forms.DefenseSessionForm(request.POST)
        if form.is_valid():
            level = form.cleaned_data['level']
            license_exists = models.DefenseSession.objects.filter(level='3rd year bachelor\'s degree').exists()
            master_exists = models.DefenseSession.objects.filter(level='2nd year master\'s degree').exists()
            
            if level == '3rd year bachelor\'s degree' and license_exists:
                messages.error(request, "Defense session for 3rd year bachelor's degree already exists.")
                return redirect('admin_choises')
            elif level == '2nd year master\'s degree' and master_exists:
                messages.error(request, "Defense session for 2nd year master's degree already exists.")
                return redirect('admin_choises')

            form.save()
            messages.success(request, "Defense session created successfully.")
            return redirect('admin_choises')
    else:
        form = forms.DefenseSessionForm()
    return render(request, 'gestionpfe/create_defense_session.html', {'form': form, 'admin': admin})


logger = logging.getLogger(__name__)

def clean_keywords(keyword_str):
    return set(keyword.strip().lower() for keyword in keyword_str.split() if keyword.strip())

def compare_keywords(subject_keywords, teacher_keywords):
    return len(subject_keywords.intersection(teacher_keywords))

@login_required(login_url='/login_admin')
@user_passes_test(is_admin)
def schedule_defense(request, subject_choice_id):
    try:
        subject_choice = get_object_or_404(models.SubjectChoice, id=subject_choice_id)
        if subject_choice.subject.level == '3rd year bachelor\'s degree':
            session = models.DefenseSession.objects.filter(level='3rd year bachelor\'s degree').latest('end_date')
        if subject_choice.subject.level == '2nd year master\'s degree':
            session = models.DefenseSession.objects.filter(level='2nd year master\'s degree').latest('end_date')
            

        
        if not session:
                messages.error(request, "You have to create a defense session")
                return redirect('create_defense_session')
        student = subject_choice.student
        subject = subject_choice.subject
        subject_keywords = clean_keywords(subject.keyword)
        teachers = models.Teacher.objects.all()
        teacher_scores = []

        logger.info(f"Scheduling for Subject: {subject.title}, Keywords: {subject_keywords}")

        for teacher in teachers:
            teacher_keywords = clean_keywords(teacher.keyword)
            common_keywords = compare_keywords(subject_keywords, teacher_keywords)
            logger.info(f"Teacher: {teacher.get_name}, Keywords: {teacher_keywords}, Common Keywords: {common_keywords}")
            if common_keywords and teacher.id != subject.creator_id:
                teacher_scores.append((common_keywords, teacher))

        if not teacher_scores:
            teacher_scores = [(0, teacher) for teacher in teachers]
            teacher_scores.sort(key=lambda x: x[1].subject_count)
        else:
            teacher_scores.sort(key=lambda x: (x[0], -x[1].subject_count), reverse=True)

        logger.info(f"Teacher Scores: {teacher_scores}")

        if teacher_scores:
            best_teacher = teacher_scores[0][1]
            best_teacher2 = teacher_scores[1][1]
            if subject.type == 'External' and best_teacher != subject.teacher:
                best_teacher2 = subject.teacher
            

            scheduled_time = generate_suitable_time(session, best_teacher, best_teacher2)

            if scheduled_time:
                logger.info(f"Scheduled Time: {scheduled_time} for Subject: {subject.title}")
                subject_choice.affected = True
                subject_choice.save()
                defense =models.Defense.objects.create(
                    subject=subject,
                    student=student,
                    session=session,
                    scheduled_time=scheduled_time
                )
                defense.teachers.set([best_teacher, best_teacher2])
                messages.success(request, f"Subject {subject.title} has been successfully scheduled.")
            else:
                logger.warning(f"No suitable time found for Subject: {subject.title}")
                messages.warning(request, f"No suitable time found for Subject: {subject.title}")
        else:
            messages.warning(request, "No suitable teacher found for the subject")

        return redirect('admin_choises')
    except models.DefenseSession.DoesNotExist:
        messages.error(request, "You have to create a defense session")
        return redirect('create_defense_session')

def generate_suitable_time(session, jury1, jury2):
    start_date = session.start_date
    end_date = session.end_date

    while start_date < end_date:
        hour = random.randint(8, 15)
        minute = random.choice([0])
        potential_time = timezone.make_aware(datetime.datetime.combine(start_date.date(), time(hour, minute)))

        if potential_time < start_date or potential_time + timedelta(hours=1) > end_date:
            start_date += timedelta(days=1)
            continue

        

        # Check for conflicts with other scheduled defenses for the jurys
        if not models.Defense.objects.filter(scheduled_time=potential_time, teachers__in=[jury1, jury2]).exists():
            return potential_time

        start_date += timedelta(hours=1)  # Try another slot on the same day

    return None  # No suitable time found

@login_required
@user_passes_test(lambda u: is_admin(u) or is_teacher(u))
def view_defenses(request):
     
    search_term = request.GET.get('search_term', '')
    filter_value = request.GET.get('filter', '')
    
    if is_teacher(request.user):
        admin =models.Teacher.objects.filter(user=request.user)
        defenses = models.Defense.objects.filter(teachers=request.user.teacher)
        defenses_totale = defenses.count()
    if is_admin(request.user):
        admin = models.Admin.objects.filter(user=request.user)
        defenses = models.Defense.objects.all()
        defenses_totale = defenses.count()

    if search_term:
        defenses = defenses.filter(
            
            Q(student__user__first_name__icontains=search_term) |
            Q(student__user__last_name__icontains=search_term)
        )

    if filter_value in ['L3', 'M2']:
        defenses = defenses.filter(student__level=filter_value)
    elif filter_value in ['External', 'Internal']:
        defenses = defenses.filter(subject__type=filter_value)
    current_date = timezone.now()
    if is_teacher(request.user):
        for defense in defenses:
            results_count = models.Result.objects.filter(defense=defense, teacher=request.user.teacher).count()
            max_results_allowed = 1 + (defense.student.binome is not None)
            defense.can_grade = current_date > defense.scheduled_time and results_count < max_results_allowed

    paginator = Paginator(defenses, 7)  # Adjust the number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, 'gestionpfe/admin_view_defenses.html', {
        'admin':admin,
        'defenses':defenses_totale,
        'page_obj': page_obj,
        'search_term': search_term,
        'current_date': current_date,
        'filter': filter_value
    })

@login_required
@user_passes_test(is_admin)
def view_defenses_session(request):
    admin = models.Admin.objects.filter(user=request.user)
    defenses_session = models.DefenseSession.objects.all()
    return render(request, 'gestionpfe/admin_view_defenses_session.html', {'admin':admin,'defenses': defenses_session})



###################################################################################################################
#---------------------------------------ENTREPRISE----------------------------------------------------#
###################################################################################################################


def assign_teacher_to_subject(subject):
    
        
        
        
        subject_keywords = clean_keywords(subject.keyword)
        teachers = models.Teacher.objects.all()
        teacher_scores = []

        logger.info(f"Scheduling for Subject: {subject.title}, Keywords: {subject_keywords}")

        for teacher in teachers:
            teacher_keywords = clean_keywords(teacher.keyword)
            common_keywords = compare_keywords(subject_keywords, teacher_keywords)
            logger.info(f"Teacher: {teacher.get_name}, Keywords: {teacher_keywords}, Common Keywords: {common_keywords}")
            if common_keywords and teacher.id != subject.creator_id:
                teacher_scores.append((common_keywords, teacher))

        if not teacher_scores:
            teacher_scores = [(0, teacher) for teacher in teachers]
            teacher_scores.sort(key=lambda x: x[1].subject_count)
        else:
            teacher_scores.sort(key=lambda x: (x[0], -x[1].subject_count), reverse=True)

        logger.info(f"Teacher Scores: {teacher_scores}")

        if teacher_scores:
            subject.teacher = teacher_scores[0][1]
        else:
            subject.teacher = random(teachers)

    


@login_required(login_url='login_entreprise')
@user_passes_test(is_company)
def company_update_company_view(request, pk):
    teacher=models.Enterprise.objects.filter(user = request.user.id)
    ent = models.Enterprise.objects.get(id=pk)
    user = models.User.objects.get(id=ent.user_id)

    userForm = forms.SigupEntForm(instance=user, initial={
        'username': user.username,
        'email': user.email,
        
    })
    entForm = forms.EntrepriseForm(instance=ent, initial={
        'name': ent.name,
        
    })
    
    

    if request.method == 'POST':
        userForm = forms.SigupEntForm(request.POST, instance=user)
        entForm = forms.EntrepriseForm(request.POST, instance=ent)
        
        if entForm.is_valid():
            ent = entForm.save(commit=False)
            if userForm.has_changed():
                if userForm.is_valid():
                    user = userForm.save()
                    ent.user = user
            ent.status = True 
            ent.save()
            return redirect('teacher_subject')
    else :
        userForm = forms.SigupEntForm(instance=user)
        entForm = forms.EntrepriseForm(instance=ent)
    
    return render(request, 'gestionpfe/company_update_company.html', {'userForm': userForm, 'admin':teacher,'entForm':entForm,'ent':ent})



######################################################################################################################
#-------------------------------------------------TEACHER----------------------------------------------------#
######################################################################################################################

@login_required(login_url='login_teacher')
@user_passes_test(is_teacher)
def teacher_update_teacher_view(request, pk):
    teacher=models.Teacher.objects.filter(user = request.user.id)
    ent = models.Teacher.objects.get(id=pk)
    user = models.User.objects.get(id=ent.user_id)

    userForm = forms.SigupForm(instance=user, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        
    })
    entForm = forms.TeacherForm(instance=ent, initial={
        'belongs': ent.belongs,
        'keyword': ent.keyword,
    })
    
    

    if request.method == 'POST':
        userForm = forms.SigupForm(request.POST, instance=user)
        entForm = forms.TeacherForm(request.POST, instance=ent)
        
        if entForm.is_valid():
            ent = entForm.save(commit=False)
            if userForm.has_changed():
                if userForm.is_valid():
                    user = userForm.save()
                    ent.user = user
            ent.keyword = entForm.cleaned_data['keyword']
            ent.status = True 
            ent.save()
            return redirect('teacher_subject')
    else :
        userForm = forms.SigupForm(instance=user)
        entForm = forms.TeacherForm(instance=ent)
    
    return render(request, 'gestionpfe/teacher_update_teacher.html', {'userForm': userForm, 'admin':teacher,'entForm':entForm,'ent':ent})

@login_required
@user_passes_test(lambda u: is_company(u) or is_teacher(u))
def teacher_add_subject_view(request):
    if is_teacher(request.user):
        teacher=models.Teacher.objects.filter(user = request.user.id)
        creator = request.user.teacher
        creator_type = ContentType.objects.get_for_model(models.Teacher)
        user_group = 'teacher'
    elif is_company(request.user):
        teacher=models.Enterprise.objects.filter(user = request.user.id)
        creator = request.user.enterprise
        creator_type = ContentType.objects.get_for_model(models.Enterprise)
        user_group = 'company'
    else:
        return redirect('teacher_subject')  

    if request.method == 'POST':
        form = forms.SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.creator = creator
            subject.creator_type = creator_type
            subject.creator_id = creator.id

            if user_group == 'teacher':
                subject.teacher = request.user.teacher
                subject.type = 'Internal'
            elif user_group == 'company':
                assign_teacher_to_subject(subject)
                subject.type = 'External'
            
            subject.status = 'PENDING'
            subject.save()
            

            all_teachers = list(models.Teacher.objects.exclude(id__in=[subject.creator_id, subject.teacher_id]))
            commission = random.sample(all_teachers, 2)
            subject.validation_commission.set(commission)
            subject.save()
            
            return redirect('teacher_subject')
    else:
        form = forms.SubjectForm()

    return render(request, 'gestionpfe/teacher_add_subject.html', {'form': form, 'admin': teacher})

@login_required
@user_passes_test(lambda u: is_company(u) or is_teacher(u))
def teacher_update_subject_view(request, pk):
    if is_teacher(request.user):
        teacher = models.Teacher.objects.filter(user=request.user.id)
    elif is_company(request.user):
        teacher = models.Enterprise.objects.filter(user=request.user.id)

    subject = models.Subject.objects.get(id=pk)
    form = forms.SubjectForm(instance=subject)
    if request.method == 'POST':
        form = forms.SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.status = 'PENDING'
            subject.rejection_reason = ''
            models.SubjectInteraction.objects.filter(subject=subject , action='rejected').delete()
            subject.save()
            return redirect('teacher_subject')
    return render(request, 'gestionpfe/teacher_update_subject.html', {'form': form, 'admin': teacher})

@login_required
@user_passes_test(lambda u: is_company(u) or is_teacher(u))
def teacher_view_subject_details(request, pk):
    if is_teacher:
        teacher=models.Teacher.objects.filter(user = request.user.id)
    elif is_company:
        teacher=models.Entreprise.objects.filter(user = request.user.id)
        
    subject = models.Subject.objects.get(id=pk)
    Form = forms.SubjectviewForm(instance=subject , initial={
        'speciality' : subject.speciality.get_name,
        'teacher' : subject.teacher.get_name,
    })
    return render(request, 'gestionpfe/teacher_view_subject_details.html', {'form':Form, 'admin':teacher})



@login_required
@user_passes_test(lambda u: is_company(u) or is_teacher(u))
def teacher_view_subject_view(request):
    admin = None
    subjects = None
    total_subjects = pending_subjects = 0
    content_type = None
    
    if is_teacher(request.user):
        user_teacher = request.user.teacher
        if not user_teacher.keyword:  
            return redirect('teacher_add_keyword')
        admin = models.Teacher.objects.filter(user=request.user)
        content_type = ContentType.objects.get_for_model(models.Teacher)
        creator_id = user_teacher.id
    elif is_company(request.user):
        user_enterprise = request.user.enterprise
        admin = models.Enterprise.objects.filter(user=request.user)
        content_type = ContentType.objects.get_for_model(models.Enterprise)
        creator_id = user_enterprise.id

    if content_type:
        subjects = models.Subject.objects.filter(
            creator_id=creator_id,
            creator_type=content_type
        )
        total_subjects = subjects.count()
        pending_subjects = subjects.filter(status='PENDING').count()

    search_term = request.GET.get('search_term', '')
    filter_value = request.GET.get('filter', '')
    
    if search_term:
        subjects = subjects.filter(title__icontains=search_term)

    if filter_value:
        if filter_value in ['L3', 'M2']:
            subjects = subjects.filter(level=filter_value)
        elif filter_value in ['PENDING', 'APPROVED', 'REJECTED']:
            subjects = subjects.filter(status=filter_value)

    paginator = Paginator(subjects, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, 'gestionpfe/teacher_view_subject.html', {
        'subjects': subjects, 
        'search_term': search_term, 
        'admin': admin,
        'filter': filter_value,
        'page_obj': page_obj, 
        'pending_subjects': pending_subjects,
        'total_subjects': total_subjects
    })

@login_required(login_url='login_teacher')
def add_keyword_view(request):
    teacher = request.user.teacher
    admin = models.Teacher.objects.filter(user=request.user)

    if request.method == 'POST':
        form = forms.TeacherKeywordsForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keyword']
            teacher.keyword = keywords
            teacher.save()
            return redirect('teacher_subject')

    else:
        form = forms.TeacherKeywordsForm()

    return render(request, 'gestionpfe/teacher_add_keyword.html', {'form': form, 'admin':admin})

@login_required(login_url='login_teacher')
def update_keyword_view(request):
    teacher = request.user.teacher
    admin = models.Teacher.objects.filter(user=request.user)

    if request.method == 'POST':
        form = forms.TeacherKeywordsForm(request.POST,instance=teacher)
        if form.is_valid():
            keywords = form.cleaned_data['keyword']
            teacher.keyword = keywords
            teacher.save()
            return redirect('teacher_subject')

    else:
        form = forms.TeacherKeywordsForm(instance=teacher)

    return render(request, 'gestionpfe/teacher_update_keyword.html', {'form': form, 'admin':admin})



@login_required(login_url='login_teacher')
@user_passes_test(is_teacher)
def assigned_subjects_view(request):
    search_term = request.GET.get('search_term', '')
    filter_value = request.GET.get('filter', '')
    admin = models.Teacher.objects.filter(user=request.user)
    teacher = request.user.teacher
    assigned_subjects = models.SubjectChoice.objects.filter(subject__teacher=teacher, validated_by_student=True)

    if search_term:
        assigned_subjects = models.SubjectChoice.objects.filter(
            Q(subject__title__icontains=search_term),
            subject__teacher=teacher, validated_by_student=True
        )
    
    if filter_value:
        assigned_subjects = assigned_subjects.filter(subject__level=filter_value)

    paginator = Paginator(assigned_subjects, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gestionpfe/teacher_assigned_subjects.html', {'page_obj': page_obj, 'admin':admin})

@login_required(login_url='login_teacher')
@user_passes_test(is_teacher)
def teacher_gives_grade(request, pk):
    admin = models.Teacher.objects.filter(user=request.user)
    defense = get_object_or_404(models.Defense, id=pk)
    teacher = request.user.teacher
    
   
    

    if request.method == 'POST':
        form = forms.ResultForm(request.POST, defense_id=pk)
        if form.is_valid():
            student = form.cleaned_data['student_choice']
            new_note = form.cleaned_data['note']

            if new_note > 20:
                form.add_error('note', ValidationError('Grade cannot exceed 20.'))
            else:
                subject = defense.subject

                # Create a new result
                result = models.Result(note=new_note, defense=defense, teacher=teacher)
                result.save()

                return redirect('view_defenses')
    else:
        form = forms.ResultForm(defense_id=pk, teacher=teacher)

    return render(request, 'gestionpfe/teacher_give_grade.html', {'form': form, 'defense': defense, 'admin': admin})

@login_required(login_url='login_teacher')
@user_passes_test(is_teacher)
def teacher_add_summary(request, pk):
    admin = models.Teacher.objects.filter(user=request.user)
    choice = models.SubjectChoice.objects.get(id=pk)
    
    initial_data = {
        'student': choice.student.get_name,
        'student2': choice.student.binome.get_name if choice.student.binome else '',
        'title': choice.subject.title,
    }

    if request.method == 'POST':
        form = forms.SuiviForm(request.POST)
        if form.is_valid():
            summary = form.save(commit=False)
            summary.choice = choice 
            summary.resume = form.cleaned_data['resume']
            summary.save()
            return redirect('teacher_assigned_subject')
    else:
        form = forms.SuiviForm(initial=initial_data)

    return render(request, 'gestionpfe/teacher_add_summary.html', {'form': form, 'choice': choice, 'admin': admin})

@login_required(login_url='login_teacher')
@user_passes_test(is_teacher)
def teacher_approve_defence(request,pk):
    choice = models.SubjectChoice.objects.get(id=pk)
    choice.teacheraprove = 'allowed'
    choice.save()
    return redirect('teacher_assigned_subject')

@login_required(login_url='login_teacher')
@user_passes_test(is_teacher)
def teacher_delete_defence(request,pk):
    choice = models.SubjectChoice.objects.get(id=pk)
    choice.teacheraprove = 'not-allowed'
    choice.save()
    return redirect('teacher_assigned_subject')



######################################################################################################################
#-------------------------------------------------student----------------------------------------------------#
######################################################################################################################

@login_required(login_url='login_student')
@user_passes_test(is_student)
def student_view_subject_view(request):
    admin = models.Student.objects.filter(user=request.user)
    search_term = request.GET.get('search_term', '')
    total_subjects = models.Subject.objects.filter(
        level=request.user.student.level,
        speciality=request.user.student.speciality,
        status='APPROVED',
        valable=True
    ).count()


    user_student = request.user.student
    binome = user_student.binome or user_student  # Utiliser le binôme si disponible, sinon l'étudiant lui-même
    
    # Obtenir les IDs des sujets déjà choisis par le binôme/monôme
    chosen_subject_ids = models.SubjectChoice.objects.filter(
        student=binome
    ).values_list('subject__id', flat=True)

    # Filtrer les sujets qui ne sont pas encore choisis
    query = models.Subject.objects.filter(
        level=user_student.level,
        speciality=user_student.speciality,
        status='APPROVED',
        valable=True
    ).exclude(id__in=chosen_subject_ids)  # Exclure les sujets déjà choisis

    if search_term:
        query = query.filter(
            Q(title__icontains=search_term) 
        )
    
    # Pagination
    paginator = Paginator(query, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestionpfe/student_view_subject.html', {'page_obj': page_obj, 'search_term': search_term ,'total_subjects':total_subjects,'admin':admin})

@login_required(login_url='login_student')
@user_passes_test(is_student)
def add_subject_to_choices(request, subject_id):
    user_student = request.user.student
    binome = user_student.binome 

    if (models.SubjectChoice.objects.filter(student=user_student).count() + models.SubjectChoice.objects.filter(student=binome).count() )==3:
        messages.error(request, "You can only choose three subject.")
        return redirect('student_view_subject')

    subject = get_object_or_404(models.Subject, id=subject_id, valable=True)
    models.SubjectChoice.objects.create(student=user_student, subject=subject)
    subject.valable = False  # Marquer le sujet comme non disponible pour les autres
    subject.save()
    
    messages.success(request, "Subject added to your choices.")
    return redirect('student_view_subject')

@login_required(login_url='login_student')
@user_passes_test(is_student)
def remove_subject_from_choices(request, choice_id):
    user_student = request.user.student
    binome = user_student.binome  

    try:
        # Try to get the SubjectChoice for the binome or the user_student
        subject_choice = models.SubjectChoice.objects.filter(
            id=choice_id, 
            student__in=[binome, user_student]
        ).first()
        
        if subject_choice:
            subject_choice.subject.valable = True
            subject_choice.subject.save()  # Make sure to save the subject after updating the 'valable' attribute
            subject_choice.delete()
            messages.success(request, "Subject has been removed from your choices.")
        else:
            messages.error(request, "You do not have permission to remove this subject.")
    except models.SubjectChoice.DoesNotExist:
        messages.error(request, "The selected subject was not found in your choices.")

    return redirect('student_view_choices')

@login_required(login_url='login_student')
@user_passes_test(is_student)
def view_binome_choices(request):
    admin = models.Student.objects.filter(user=request.user)
    user_student = request.user.student
    binome = user_student.binome
    
    binome_choices = models.SubjectChoice.objects.filter(student=binome)
    user_choices = models.SubjectChoice.objects.filter(student=user_student)

    choices = list(binome_choices) + list(user_choices)
    
    
    return render(request, 'gestionpfe/student_view_binome_choices.html', {'choices': choices,'admin':admin})
    

@login_required(login_url='login_student')
@user_passes_test(is_student)
def validate_choices(request, choice_id):
    user_student = request.user.student
    binome = user_student.binome

    try:
        subject_choice = models.SubjectChoice.objects.filter(
            student__in=[binome, user_student], id=choice_id
        ).first()

        if not subject_choice:
            raise models.SubjectChoice.DoesNotExist

        # Check if there is no already validated choice for binome or user_student
        if not models.SubjectChoice.objects.filter(
            student__in=[binome, user_student], validated_by_student=True
        ).exists():
            # Validate the selected subject_choice
            subject_choice.validated_by_student = True
            subject_choice.save()

            # Reset other subjects
            other_choices = models.SubjectChoice.objects.filter(
                student__in=[binome, user_student], validated_by_student=False
            ).exclude(id=choice_id)

            for choice in other_choices:
                choice.subject.valable = True
                choice.subject.save()
                choice.delete()

            messages.success(request, "Your choice has been validated successfully.")
        
    except models.SubjectChoice.DoesNotExist:
        messages.error(request, "No subject choice to validate.")

    return redirect('/afterlogin')

@login_required(login_url='login_student')
@user_passes_test(is_student)
def student_subject_details_view(request):
    admin = models.Student.objects.filter(user=request.user)
    user_student = request.user.student
    binome = user_student.binome 
    defense = models.Defense.objects.filter(Q(student=user_student) | Q(student=binome)).first()
    
    if defense:
        # Calculer l'agrégat des résultats pour la défense
        result_aggregate = models.Result.objects.filter(defense=defense).aggregate(
            total_sum=Sum('note'),
            count=Count('id')
        )

        total_sum = result_aggregate['total_sum'] or 0
        count = result_aggregate['count'] or 1  # Eviter la division par zéro

        # Calculer le résultat final
        final_result = total_sum / count
    else:
        final_result = 0
    
    subject_choice = models.SubjectChoice.objects.filter(Q(student=binome)|Q(student=user_student), validated_by_student=True).first()

    
    return render(request, 'gestionpfe/student_subject_details.html', {
            'subject_choice': subject_choice,
            'admin': admin,
            'result': final_result,
            'defense': defense
      })
    


@login_required(login_url='login_student')
@user_passes_test(is_student)
def student_list_view(request):
    admin = models.Student.objects.filter(user=request.user)
    current_student = request.user.student
    students = models.Student.objects.filter(level=current_student.level, speciality=current_student.speciality, status=True)

    # Exclude the current student and students who already have a binome
    students = students.exclude(Q(id=current_student.id) | Q(binome__isnull=False))
    student_graduate = models.SubjectChoice.objects.filter(validated_by_student = True).values_list('student_id', flat=True)

    # Exclude students who have received a binome request from the current student
    sent_requests = models.BinomeRequest.objects.filter(sender=current_student).values_list('receiver_id', flat=True)
    recieved_requests = models.BinomeRequest.objects.filter(receiver=current_student).values_list('sender_id', flat=True)
    students = students.exclude(id__in=sent_requests)
    students = students.exclude(id__in=recieved_requests)
    students = students.exclude(id__in=student_graduate)

    search_term = request.GET.get('search_term')
    if search_term:
        students = students.filter(Q(user__first_name__icontains=search_term) | Q(user__last_name__icontains=search_term))

    paginator = Paginator(students, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    binome = current_student.binome

    if binome:
        return redirect('students_view_binome')
    
    return render(request, 'gestionpfe/student_list.html', {'page_obj': page_obj, 'search_term': search_term,'admin':admin})

@login_required(login_url='login_student')
@user_passes_test(is_student)
def send_binome_request_view(request, pk):
    if request.method == 'POST':
        receiver_id = pk
        receiver = models.Student.objects.get(pk=receiver_id)
        sender = request.user.student
        existing_request = models.BinomeRequest.objects.filter(sender=sender, receiver=receiver).exists()
        if existing_request:
            
            return redirect('students_available')
        binome_request = models.BinomeRequest(sender=sender, receiver=receiver)
        binome_request.save()

        messages.success(request, 'The request for a pair was sent successfully.')
        return redirect('students_available')

    return redirect('students_available')

@login_required(login_url='login_student')
@user_passes_test(is_student)
def binome_requests_view(request):
    admin = models.Student.objects.filter(user=request.user)
    
     
    search_term = request.GET.get('search_term')
    if search_term:
        students = students.filter(Q(user__first_name__icontains=search_term) | Q(user__last_name__icontains=search_term))
    binome_requests = models.BinomeRequest.objects.filter(receiver=request.user.student, status='PENDING')
    paginator = Paginator(binome_requests, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gestionpfe/student_request_received.html', {'page_obj': page_obj,'admin':admin})

@login_required(login_url='login_student')
@user_passes_test(is_student)
def accept_binome_request_view(request, pk):
    binome_request = models.BinomeRequest.objects.get(id= pk)

   
    if binome_request.receiver == request.user.student:
        binome_request.status = 'ACCEPTED'
        binome_request.save()
        other_requests = models.BinomeRequest.objects.filter(receiver= binome_request.receiver).exclude(id=pk)
        other_requests.update(status='REJECTED')
        other_requests = models.BinomeRequest.objects.filter(sender= binome_request.receiver).exclude(id=pk)
        other_requests.update(status='REJECTED')
        other_requests = models.BinomeRequest.objects.filter(sender= binome_request.sender).exclude(id=pk)
        other_requests.update(status='REJECTED')
        other_requests = models.BinomeRequest.objects.filter(receiver= binome_request.sender).exclude(id=pk)
        other_requests.update(status='REJECTED')
        sender = binome_request.sender
        receiver = binome_request.receiver
        sender.binome = receiver
        sender.save()
        receiver.binome = sender
        receiver.save()

    return redirect('students_view_binome')

@login_required(login_url='login_student')
@user_passes_test(is_student)
def reject_binome_request_view(request, pk):
    binome_request = get_object_or_404(models.BinomeRequest, id=pk)

    if binome_request.receiver == request.user.student:
        binome_request.status = 'REJECTED'
        binome_request.save()

    return redirect('students_view_request')

@login_required(login_url='login_student')
@user_passes_test(is_student)
def binome_info_view(request):
    admin = models.Student.objects.filter(user=request.user)
    current_student = request.user.student

    
    if current_student.binome:
        
        binome_info = {
            'fname': current_student.binome.user.first_name,
            'lname': current_student.binome.user.last_name,
            'level': current_student.binome.level,
            'speciality': current_student.binome.speciality,
        }
    else:
        binome_info = None 

    return render(request, 'gestionpfe/student_view_binome_info.html', {'binome_info': binome_info,'admin':admin})



@login_required(login_url='login_student')
@user_passes_test(is_student)
def student_update_student_view(request, pk):
    admin = models.Student.objects.filter(user=request.user.id)
    student = models.Student.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)

    userForm = forms.SigupForm(instance=user, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
    })
    studentForm = forms.StudentForm(instance=student)

    if request.method == 'POST':
        userForm = forms.SigupForm(request.POST, instance=user)
        studentForm = forms.StudentForm(request.POST, instance=student)

        if studentForm.is_valid():
            student = studentForm.save(commit=False)
            if userForm.has_changed():
                if userForm.is_valid():
                    user = userForm.save()
                    student.user = user
            student.status = True
            student.save()
            return redirect('student_view_subject')
    else:
        userForm = forms.SigupForm(instance=user)
        studentForm = forms.StudentForm(instance=student)

    return render(request, 'gestionpfe/student_update_student.html', {'userForm': userForm, 'admin': admin, 'studentForm': studentForm, 'student': student})
    

