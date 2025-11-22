"""
URL configuration for gestionpfe project.

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
from django.contrib import admin
from django.urls import path
from gestionpfe_app import views
from django.contrib.auth.views import LoginView,LogoutView
from gestionpfe_app.forms import LoginForm , AdminLoginForm, TeacherLoginForm, StudentLoginForm, EnterpriseLoginForm

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.home_view , name=''),
    path('contact/', views.contact_view,name='contact' ),
    path('about/', views.about_view ,name='about'),

    path('login_choose/', views.login_choose_view,name='login_choose' ),
    path('signup_choose/', views.signup_choose_view ,name='signup_choose'),

    path('signup_admin/', views.signup_admin_view ),
    path('signup_teacher/', views.signup_teacher_view ),
    path('signup_student/', views.signup_student_view ),
    path('signup_entreprise/', views.signup_entreprise_view ),

    path('login_admin/', LoginView.as_view(template_name='gestionpfe/login-admin.html', authentication_form=AdminLoginForm), name='login_admin'),
    path('login_teacher/', LoginView.as_view(template_name='gestionpfe/login-ens.html', authentication_form=TeacherLoginForm), name='login_teacher'),
    path('login_student/', LoginView.as_view(template_name='gestionpfe/login-etd.html', authentication_form=StudentLoginForm), name='login_student'),
    path('login_entreprise/', LoginView.as_view(template_name='gestionpfe/login-ent.html', authentication_form=EnterpriseLoginForm), name='login_entreprise'),


    path('afterlogin/', views.afterlogin_view,name='afterlogin'),
    path('logout/', views.logout_view, name='logout'),

    path('admin_dashboard/', views.admin_dashboard_view,name='admin_dashboard'),
    path('admin_users/', views.admin_admin_view,name='admin_users'),
    
    path('add-admin/', views.add_admin_view,name='add-admin'),
    path('update-admin/<int:pk>', views.update_admin_view,name='update-admin'),
    path('delete-admin/<int:pk>', views.delete_admin_view,name='delete-admin'),
    path('approve-admin/<int:pk>', views.approve_admin_view,name='approve-admin'),
    
    path('admin_entreprise/', views.admin_entreprise_view,name='admin_entreprise'),
    path('update-entreprise/<int:pk>', views.update_entreprise_view,name='update-entreprise'),
    path('delete-entreprise/<int:pk>', views.delete_entreprise_view,name='delete-entreprise'),
    path('approve-entreprise/<int:pk>', views.approve_entreprise_view,name='approve-entreprise'),
    path('add-entreprise/', views.add_entreprise_view,name='add-entreprise'),


    path('admin_department/', views.admin_department_view,name='admin_department'),
    path('update-department/<int:pk>', views.update_department_view,name='update-department'),
    path('delete-department/<int:pk>', views.delete_department_view,name='delete-department'),
    path('add-department/', views.add_department_view,name='add-department'),
    

    path('admin_speciality/', views.admin_speciality_view,name='admin_speciality'),
    path('update-speciality/<int:pk>', views.update_speciality_view,name='update-speciality'),
    path('delete-speciality/<int:pk>', views.delete_speciality_view,name='delete-speciality'),
    path('add-speciality/', views.add_speciality_view,name='add-speciality'),

    path('admin_teacher/', views.admin_teacher_view,name='admin_teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('add-teacher/', views.add_teacher_view,name='add-teacher'),

    path('admin_student/', views.admin_student_view,name='admin_student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    path('add-student/', views.add_student_view,name='add-student'),

    path('admin_subject/', views.admin_subject_view,name='admin_subject'),
    path('approve_subject/<int:pk>', views.approve_subject_view,name='approve-subject'),
    path('reject_subject/<int:pk>', views.reject_subject_view,name='reject-subject'),
    path('view_subject/<int:pk>', views.view_subject_view,name='view-subject'),

    path('admin_choices/', views.admin_view_validated_choices,name='admin_choises'),
    path('create_defense_session/', views.create_defense_session,name='create_defense_session'),
    path('admin_affect/<int:subject_choice_id>/', views.schedule_defense, name='admin_affect_subject'),
    path('view_defenses_session/', views.view_defenses_session,name='view_defenses_session'),
    path('view_summary/<int:pk>', views.admin_view_summary,name='view-summary'),
    


    path('view_defenses/', views.view_defenses,name='view_defenses'),


    path('teacher-update-teacher/<int:pk>', views.teacher_update_teacher_view,name='teacher-update-teacher'),
    path('teacher-summary/<int:pk>', views.teacher_add_summary,name='teacher-summary'),
    path('teacher_allowed_to_defence/<int:pk>', views.teacher_approve_defence,name='teacher-approve-choice'),
    path('teacher_dont_allow_to_defence/<int:pk>', views.teacher_delete_defence,name='teacher-delete-choice'),
    path('teacher-gives-grade/<int:pk>', views.teacher_gives_grade,name='teacher-gives-the-grade'),
    path('teacher_subject/', views.teacher_view_subject_view,name='teacher_subject'),
    path('teacher_add_subject/', views.teacher_add_subject_view,name='teacher_add_subject'),
    path('teacher_update_subject/<int:pk>', views.teacher_update_subject_view,name='teacher_update_subject'),
    path('teacher_view_subject_details/<int:pk>', views.teacher_view_subject_details,name='teacher_view_subject_details'),
    path('teacher_assigned_subject/', views.assigned_subjects_view,name='teacher_assigned_subject'),
    path('teacher_add_keyword/', views.add_keyword_view,name='teacher_add_keyword'),
    path('teacher_update_keyword/', views.update_keyword_view,name='teacher_update_keyword'),

    path('company-update-company/<int:pk>', views.company_update_company_view,name='company-update-company'),
    

    path('student_view_subject/', views.student_view_subject_view,name='student_view_subject'),
    path('add-subject-to-choices/<int:subject_id>/', views.add_subject_to_choices, name='add_subject_to_choices'),
    path('remove-subject-from-choices/<int:choice_id>/', views.remove_subject_from_choices, name='remove_subject_from_choices'),
    path('student_view_choices/', views.view_binome_choices,name='student_view_choices'),
    path('student_validate_choices/<int:choice_id>/', views.validate_choices,name='student_validate_choices'),
    path('students_available/', views.student_list_view,name='students_available'),
    path('students_send_request/<int:pk>', views.send_binome_request_view,name='students_send_request'),
    path('students_view_request/', views.binome_requests_view,name='students_view_request'),
    path('students_accept_request/<int:pk>', views.accept_binome_request_view,name='students_accept_request'),
    path('students_reject_request/<int:pk>', views.reject_binome_request_view,name='students_reject_request'),
    path('students_view_binome/', views.binome_info_view,name='students_view_binome'),
    path('student_subject_details/', views.student_subject_details_view,name='student_subject_details'),
    path('student-update-student/<int:pk>', views.student_update_student_view,name='student-update-student'),
    


]
