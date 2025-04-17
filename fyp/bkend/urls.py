from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.login_view, name='login'),  # Login page
    path('register/', views.registration_form, name='registration_form'),  # Registration form page
    path('register-user/', views.register_user, name='register_user'),  # Registration form submission
    path('login/', views.user_login, name='login'),  # Login page
    path('program-selection/', views.program_selection, name='program_selection'),  # Program selection page
    path('save-program-selection/', views.save_program_selection, name='save_program_selection'),  # Save program selection
    path('basic-info/', views.basic_info, name='basic_info'),  # Basic info page
    path('save-basic-info/', views.save_basic_info, name='save_basic_info'),  # Save basic info
    path('academic-info/', views.academic_info, name='academic_info'),  # Academic info page
    path('save-academic-info/', views.save_academic_info, name='save_academic_info'),  # Save academic info
    path('financial-info/', views.financial_info, name='financial_info'),  # Financial info page
    path('save-financial-info/', views.save_financial_info, name='save_financial_info'),  # Save financial info
    path('document-uploading/', views.document_uploading, name='document-uploading'),
    path('save-documents/', views.save_documents, name='save_documents'),  # Save document uploading
    path('declaration-submission/', views.declaration_submission, name='declaration-submission'),
    path('submit-application/', views.submit_application, name='submit_application'),
    path('view-status/', views.view_status, name='view_status'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('delete-application/', views.delete_application, name='delete_application'),
    path('new-application/', views.new_application, name='new_application'),  # Note the underscore
    path('logout/', views.logout_view, name='logout'),
    path('upload-profile-pic/', views.upload_profile_pic, name='upload_profile_pic'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-applications/', views.admin_application_list, name='admin_application_list'),
    path('admin-applications/<str:status>/', views.admin_application_list, name='admin_application_list_filtered'),
    path('admin-application/<str:identity_card>/', views.admin_application_detail, name='admin_application_detail'),
    path('shortlisted-applications/', views.ShortlistedApplicationsView.as_view(), name='shortlisted_applications'),
   
   
   
    # Removed send interview email functionality for now
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)