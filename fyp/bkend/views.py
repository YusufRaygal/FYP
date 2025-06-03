from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Registration, ProgramSelection
from .models import Registration, BasicInfo
from django.utils import timezone
from django.contrib.auth import logout as auth_logout
from .models import PrescreeningCriteria, Country

# -------------------------
# RENDER PAGES
# -------------------------

def program_selection(request):
    """
    Renders the program selection page.
    Ensures the identity_card is available in the session.
    """
    identity_card = request.session.get('identity_card')  # Retrieve from session

    if not identity_card:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('user_login')

    try:
        # Get the user and their existing program selection
        user = Registration.objects.get(identity_card=identity_card)
        existing_selection = ProgramSelection.objects.filter(user=user).first()  # Get the first selection or None

        return render(request, "bkend/program-selection-info.html", {
            'identity_card': identity_card,
            'existing_selection': existing_selection  # Pass existing selection to the template
        })

    except Registration.DoesNotExist:
        messages.error(request, "User not found! Please register first.")
        return redirect('user_login')

def registration_form(request):
    # Your registration form handling logic here
    return render(request, 'bkend/registration-info.html')


def basic_info(request):
    """ Renders the basic info page with countries data. """
    # Get identity_card from session
    identity_card = request.session.get('identity_card')
    
    if not identity_card:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('user_login')

    try:
        # Get countries list
        countries = sorted([country.name for country in pycountry.countries], key=lambda x: x)
    except:
        # Fallback if pycountry fails
        countries = [
            "United States", "Canada", "United Kingdom", 
            "Australia", "Malaysia", "Singapore"
        ]
    
    try:
        # Get the Registration instance
        registration = Registration.objects.get(identity_card=identity_card)
        
        # Try to get existing user data if available
        try:
            existing_info = BasicInfo.objects.get(user=registration)
            # Format dates for HTML input
            if existing_info.birthdate:
                existing_info.birthdate = existing_info.birthdate.strftime('%Y-%m-%d')
            if existing_info.passport_issue_date:
                existing_info.passport_issue_date = existing_info.passport_issue_date.strftime('%Y-%m-%d')
            if existing_info.passport_expiry_date:
                existing_info.passport_expiry_date = existing_info.passport_expiry_date.strftime('%Y-%m-%d')
        except BasicInfo.DoesNotExist:
            existing_info = None
        
        context = {
            'countries': countries,
            'existing_info': existing_info,
            'identity_card': identity_card
        }
        
        return render(request, "bkend/basic-info.html", context)
        
    except Registration.DoesNotExist:
        messages.error(request, "User not found! Please register first.")
        return redirect('user_login')

def academic_info(request):
    """
    Renders the academic info page with existing data if available.
    """
    # 1. Verify user session
    identity_card = request.session.get('identity_card')
    if not identity_card:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('user_login')

    try:
        # 2. Get user instance
        user = Registration.objects.get(identity_card=identity_card)
        
        # 3. Get existing academic info if available
        try:
            existing_info = AcademicInfo.objects.get(user=user)
            # Format dates for HTML input
            if existing_info.start_date:
                existing_info.formatted_start_date = existing_info.start_date.strftime('%Y-%m-%d')
            if existing_info.completion_date:
                existing_info.formatted_completion_date = existing_info.completion_date.strftime('%Y-%m-%d')
        except AcademicInfo.DoesNotExist:
            existing_info = None

        # 4. Prepare country list
        try:
            countries = sorted([country.name for country in pycountry.countries], key=lambda x: x)
        except:
            countries = ["United States", "Canada", "United Kingdom", "Australia", "Malaysia", "Singapore"]

        # 5. Prepare context
        context = {
            'existing_info': existing_info,
            'identity_card': identity_card,
            'countries': countries
        }
        
        return render(request, "bkend/academic-info.html", context)
        
    except Registration.DoesNotExist:
        messages.error(request, "User account not found.")
        return redirect('user_login')
    except Exception as e:
        logger.error(f"Error loading academic info: {str(e)}")
        messages.error(request, "An error occurred while loading the form.")
        return redirect('dashboard')

def financial_info(request):
    """
    Displays the financial info form with existing data if available
    """
    # 1. Verify user session
    identity_card = request.session.get('identity_card')
    if not identity_card:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')  # Using your login URL name

    try:
        # 2. Get user instance
        user = Registration.objects.get(identity_card=identity_card)
        
        # 3. Get existing financial info if available
        try:
            existing_info = FinancialInfo.objects.get(user=user)
        except FinancialInfo.DoesNotExist:
            existing_info = None

        # 4. Prepare country list
        try:
            countries = sorted([country.name for country in pycountry.countries], key=lambda x: x)
        except:
            countries = ["United States", "Canada", "United Kingdom", "Australia", "Malaysia", "Singapore"]

        # 5. Prepare context
        context = {
            'existing_info': existing_info,
            'identity_card': identity_card,
            'countries': countries
        }
        
        return render(request, "bkend/financial-info.html", context)

    except Registration.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('dashboard')  # Using your dashboard URL name


def document_uploading(request):
    """
    Displays document upload page with existing documents (read-only for editing)
    """
    # 1. Verify user session
    identity_card = request.session.get('identity_card')
    if not identity_card:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')

    try:
        # 2. Get user instance
        user = Registration.objects.get(identity_card=identity_card)
        
        # 3. Get existing documents if available
        try:
            existing_docs = DocumentUpload.objects.get(user=user)
        except DocumentUpload.DoesNotExist:
            existing_docs = None

        # 4. Prepare context
        context = {
            'existing_docs': existing_docs,
            'identity_card': identity_card
        }
        
        return render(request, "bkend/document-uploading.html", context)

    except Registration.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('dashboard')

def declaration_submission(request):
    return render(request, "bkend/declaration-submission.html")

def login_view(request):
    return render(request, "bkend/loginpage.html")

def view_status(request):
    return render(request, "bkend/view-status.html")
def student_dashboard(request):
    return render(request, "bkend/dashboard.html")

def logout_view(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, "You have been logged out successfully")
    return redirect('login')

def home(request):
    countries = sorted([country.name for country in pycountry.countries], key=lambda x: x)
    
    # Get all prescreening criteria with their country information
    criteria_list = []
    for criteria in PrescreeningCriteria.objects.prefetch_related('countries', 'ineligible_countries').all():
        criteria_list.append({
            'name': criteria.name,
            'countries': [c.name for c in criteria.countries.all()],
            'ineligible_countries': [c.name for c in criteria.ineligible_countries.all()],
            'minimum_cgpa': criteria.minimum_cgpa,
            'minimum_age': criteria.minimum_age,
            'maximum_age': criteria.maximum_age,
            'marital_status': criteria.marital_status,
            'gender': criteria.gender
        })
    
    context = {
        'countries': countries,
        'prescreening_criteria_json': json.dumps(criteria_list)
    }
    
    return render(request, 'bkend/home.html', context)



import pycountry
def grades_view(request):
    # Fetch all countries using pycountry
    countries = [country.name for country in pycountry.countries]
    
    # Render the template with the countries list
    return render(request, 'bkend/grades.html', {'countries': countries})
# USER REGISTRATION
# -------------------------




import logging
logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Registration
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Registration
import json

from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt  # Remove in production
def register_user(request):
    if request.method != "POST":
        messages.error(request, "Only POST requests are allowed.")
        return redirect('registration_form')

    try:
        data = request.POST if request.POST else json.loads(request.body)

        required_fields = [
            'identity_card', 'first_name', 'last_name', 
            'primary_email', 'country_code', 'contact_number',
            'password', 'applicant_type'
        ]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            messages.error(request, f"Missing fields: {', '.join(missing_fields)}")
            return redirect('registration_form')

        if Registration.objects.filter(primary_email=data['primary_email']).exists():
            messages.error(request, "Email already registered")
            return redirect('registration_form')

        if Registration.objects.filter(identity_card=data['identity_card']).exists():
            messages.error(request, "Identity card already registered")
            return redirect('registration_form')

        # Create the user
        user = Registration.objects.create(
            identity_card=data['identity_card'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            primary_email=data['primary_email'].lower(),
            secondary_email=data.get('secondary_email', '').lower() or None,
            country_code=data['country_code'],
            contact_number=data['contact_number'],
            password=make_password(data['password']),
            applicant_type=data['applicant_type'],
            application_submitted=False,
            submission_date=None,
            profile_pic=None
        )

        # Send a welcome email
        subject = "Welcome to AIU Admission Portal"
        message = f"""
Hi {user.first_name},

Thank you for registering on the AIU Admission Portal. We're excited to have you on board!

You can now log in to your account using the email address you registered with:
Email: {user.primary_email}

If you have any questions, feel free to contact us.

Best regards,
AIU Admission Team
"""
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.primary_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, "Registration successful! A welcome email has been sent to your email address.")
        return redirect('login')  # or wherever the login view is named

    except json.JSONDecodeError:
        messages.error(request, "Invalid data format.")
        return redirect('registration_form')
    
    except Exception as e:
        messages.error(request, f"Unexpected error: {str(e)}")
        return redirect('registration_form')

    

# -------------------------
# USER LOGIN
# -------------------------
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os

def upload_profile_pic(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        identity_card = request.session.get('identity_card')
        if not identity_card:
            return JsonResponse({
                'success': False,
                'error': 'Session expired. Please log in again.'
            }, status=401)
            
        try:
            user = Registration.objects.get(identity_card=identity_card)
            uploaded_file = request.FILES['profile_pic']
            
            # Validate file type
            valid_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in valid_extensions:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid file type. Only JPG/PNG images are allowed.'
                }, status=400)
            
            # Validate file size (2MB max)
            if uploaded_file.size > 2 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'File too large. Maximum size is 2MB.'
                }, status=400)
            
            # Delete old file if exists (except default)
            if user.profile_pic and not user.profile_pic.name.endswith('default.jpg'):
                try:
                    if default_storage.exists(user.profile_pic.name):
                        default_storage.delete(user.profile_pic.name)
                except Exception as e:
                    print(f"Error deleting old profile pic: {e}")
            
            # Save new file
            user.profile_pic = uploaded_file
            user.save()
            
            return JsonResponse({
                'success': True,
                'url': user.profile_pic.url,
                'message': 'Profile picture updated successfully!'
            })
            
        except Registration.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'User not found.'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method or no file provided.'
    }, status=400)
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        identity_card = request.session.get('identity_card')
        if not identity_card:
            return JsonResponse({
                'success': False,
                'error': 'Session expired. Please log in again.'
            }, status=401)
            
        try:
            user = Registration.objects.get(identity_card=identity_card)
            uploaded_file = request.FILES['profile_pic']
            
            # Validate file type
            valid_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in valid_extensions:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid file type. Only JPG/PNG images are allowed.'
                }, status=400)
            
            # Validate file size (2MB max)
            if uploaded_file.size > 2 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'File too large. Maximum size is 2MB.'
                }, status=400)
            
            # Delete old file if exists (except default)
            if user.profile_pic and not user.profile_pic.name.endswith('default.jpg'):
                try:
                    if default_storage.exists(user.profile_pic.name):
                        default_storage.delete(user.profile_pic.name)
                except Exception as e:
                    print(f"Error deleting old profile pic: {e}")
            
            # Save new file
            user.profile_pic = uploaded_file
            user.save()
            
            return JsonResponse({
                'success': True,
                'url': user.profile_pic.url,
                'message': 'Profile picture updated successfully!'
            })
            
        except Registration.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'User not found.'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method or no file provided.'
    }, status=400)

def user_login(request):
    """Handle login with page-specific messages"""
    # Clear any existing messages to prevent carryover
    storage = messages.get_messages(request)
    for message in storage:
        pass  # This clears old messages
    storage.used = False  # Ensure storage can be used again

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Registration.objects.get(primary_email=email)
            
            if check_password(password, user.password):
                request.session['identity_card'] = user.identity_card
                messages.success(request, "Login successful!")
                return redirect("dashboard")  # Immediate redirect to dashboard
                
            else:
                messages.error(request, "Invalid email or password")
        except Registration.DoesNotExist:
            messages.error(request, "Invalid email or password")
    
    return render(request, "bkend/loginpage.html")

# -------------------------
# SAVE PROGRAM SELECTION
# -------------------------

def save_program_selection(request):
    """Handles saving/updating the user's program selection with AJAX support"""
    if request.method != "POST":
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        }, status=400)

    identity_card = request.POST.get('identity_card') or request.session.get('identity_card')
    
    if not identity_card:
        return JsonResponse({
            'success': False,
            'message': 'Session expired. Please log in again.'
        }, status=401)

    try:
        # Check if application is already submitted
        user = Registration.objects.get(identity_card=identity_card)
        if user.submission_date:
            return JsonResponse({
                'success': False,
                'message': 'Cannot update program selection after application submission'
            }, status=403)

        # Validate required fields
        required_fields = ['first_program', 'intake_year', 'study_mode']
        for field in required_fields:
            if not request.POST.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'Missing required field: {field.replace("_", " ")}'
                }, status=400)

        # Get or create program selection
        program_selection, created = ProgramSelection.objects.get_or_create(user=user)
        
        # Update fields
        program_selection.first_program = request.POST.get('first_program')
        program_selection.second_program = request.POST.get('second_program', '')
        program_selection.third_program = request.POST.get('third_program', '')
        program_selection.fourth_program = request.POST.get('fourth_program', '')
        program_selection.intake_year = request.POST.get('intake_year')
        program_selection.study_mode = request.POST.get('study_mode')
        
        program_selection.save()
        
        # Store success message in session for the next page
        request.session['success_message'] = "Program selection updated successfully!"
        
        return JsonResponse({
            'success': True,
            'message': 'Program selection saved successfully!'
        })

    except Registration.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found! Please register first.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import BasicInfo, Registration
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import logging
from .models import BasicInfo, Registration
from django.core.exceptions import ValidationError
import pycountry

# Set up logging
logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.urls import reverse
import pycountry
import logging

logger = logging.getLogger(__name__)

@require_POST
def save_basic_info(request):
    try:
        # Debugging country loading (can be removed in production)
        print("Attempting to load countries from pycountry...")
        try:
            test_countries = list(pycountry.countries)
            print(f"Found {len(test_countries)} countries in pycountry")
            countries = sorted([country.name for country in test_countries], key=lambda x: x)
            print(f"First 3 countries: {countries[:3]}")
        except Exception as e:
            print(f"Pycountry failed: {str(e)}")
            countries = ["Test Country 1", "Test Country 2", "Test Country 3"]

        # Get user from session
        identity_card = request.session.get('identity_card')
        if not identity_card:
            return JsonResponse({
                'success': False,
                'message': "Session expired or user not logged in.",
                'redirect_url': reverse('user_login')
            }, status=401)

        try:
            user = Registration.objects.get(identity_card=identity_card)
            print(f"Found user: {user}")
        except Registration.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': "User not found!",
                'redirect_url': reverse('basic_info')
            }, status=404)

        # Check if application is already submitted - this should be the FIRST check
        if user.submission_date:
                return JsonResponse({
        'success': False,
        'locked': True,
        'message': 'Cannot update basic information after application submission.'
    }, status=200)

        # Rest of your existing code for handling the save operation...
        try:
            existing_info = BasicInfo.objects.get(user=user)
            print(f"Found existing info for user: {existing_info}")
        except BasicInfo.DoesNotExist:
            existing_info = None
            print("No existing info found for user")

        # Debug: Print raw POST data
        print("\n=== RAW POST DATA ===")
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        # Create new BasicInfo or update existing one
        basic_info = existing_info if existing_info else BasicInfo(user=user)

        # Set required fields with validation
        required_fields = {
            'birthdate': request.POST.get('birthdate'),
            'country': request.POST.get('country'),
            'country_of_birth': request.POST.get('country_of_birth'),
            'nationality': request.POST.get('nationality'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'postcode': request.POST.get('postcode'),
            'gender': request.POST.get('gender'),
            'religion': request.POST.get('religion'),
            'marital_status': request.POST.get('marital_status'),
            'passport_issue_date': request.POST.get('passport_issue_date'),
            'passport_issue_place': request.POST.get('passport_issue_place'),
            'passport_expiry_date': request.POST.get('passport_expiry_date'),
            'transferring_institution': request.POST.get('transferring_institution'),
            'siblings_count': request.POST.get('siblings_count')
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'message': f"Missing required fields: {', '.join(missing_fields)}"
            }, status=400)

        # Update all fields from POST data
        field_mapping = {
            'address': 'address',
            'city': 'city',
            'postcode': 'postcode',
            'country': 'country',
            'gender': 'gender',
            'religion': 'religion',
            'marital_status': 'marital_status',
            'birthdate': 'birthdate',
            'country_of_birth': 'country_of_birth',
            'siblings_count': 'siblings_count',
            'nationality': 'nationality',
            'skype_account': 'skype_account',
            'transferring_institution': 'transferring_institution',
            'disability_info': 'disability_info',
            'allergies_info': 'allergies_info',
            'passport_issue_date': 'passport_issue_date',
            'passport_issue_place': 'passport_issue_place',
            'has_malaysian_pass': 'has_malaysian_pass',
            'passport_expiry_date': 'passport_expiry_date',
        }

        for form_field, model_field in field_mapping.items():
            value = request.POST.get(form_field)
            if value is not None:
                # Handle boolean fields
                if form_field in ['transferring_institution', 'has_malaysian_pass']:
                    value = value.lower() == 'true'
                setattr(basic_info, model_field, value)

        # Validate and save
        try:
            basic_info.full_clean()
            basic_info.save()
            
            print("Basic info saved successfully!")
            
            return JsonResponse({
                'success': True,
                'message': "Basic information saved successfully!",
                'redirect_url': reverse('academic_info')
            })

        except ValidationError as e:
            print("\n=== VALIDATION ERRORS ===")
            print(e.message_dict)
            
            error_messages = []
            for field, errors in e.message_dict.items():
                error_messages.append(f"{field}: {', '.join(errors)}")
            
            return JsonResponse({
                'success': False,
                'message': "Validation errors: " + "; ".join(error_messages)
            }, status=400)

    except Exception as e:
        logger.exception("Error saving basic info")
        return JsonResponse({
            'success': False,
            'message': f"An error occurred: {str(e)}" if settings.DEBUG else "An error occurred while saving. Please try again."
        }, status=500)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import AcademicInfo, Registration
import logging

logger = logging.getLogger(__name__)

from django.http import JsonResponse

def save_academic_info(request):
    if request.method == 'POST':
        try:
            identity_card = request.session.get('identity_card')
            if not identity_card:
                return JsonResponse({
                    'success': False,
                    'message': "Session expired. Please log in again.",
                    'redirect_url': reverse('user_login')
                }, status=401)
            
            try:
                user = Registration.objects.get(identity_card=identity_card)
            except Registration.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': "User account not found.",
                    'redirect_url': reverse('academic_info')
                }, status=404)

            # Handle submission lock
            if user.submission_date:
                return JsonResponse({
                    'success': False,
                    'locked': True,
                    'message': "Cannot update academic information after application submission."
                }, status=200)

            academic_info, _ = AcademicInfo.objects.get_or_create(user=user)

            academic_info.high_school_level = request.POST.get('high_school_level')
            academic_info.high_school_name = request.POST.get('high_school_name')
            academic_info.high_school_address = request.POST.get('high_school_address')
            academic_info.high_school_country = request.POST.get('high_school_country')
            academic_info.english_score = request.POST.get('english_score')
            academic_info.math_score = request.POST.get('math_score')
            academic_info.highest_qualification = request.POST.get('highest_qualification')
            academic_info.program_name = request.POST.get('program_name')
            academic_info.cgpa_score = request.POST.get('cgpa_score')  # Keep only CGPA score

            academic_info.institution_name = request.POST.get('institution_name')
            academic_info.start_date = request.POST.get('start_date') or None
            academic_info.completion_date = request.POST.get('completion_date') or None
            academic_info.national_language = request.POST.get('national_language')

            if academic_info.national_language == 'NON_ENGLISH':
                academic_info.english_test_type = request.POST.get('english_test_type', '')
                academic_info.test_year = request.POST.get('test_year', '')
                academic_info.band_score = request.POST.get('band_score', '')
            else:
                academic_info.english_test_type = None
                academic_info.test_year = None
                academic_info.band_score = None

            academic_info.full_clean()
            academic_info.save()

            return JsonResponse({
                'success': True,
                'message': "Academic information saved successfully!",
                'redirect_url': reverse('financial_info')
            })

        except ValidationError as e:
            errors = [f"{field}: {', '.join(errs)}" for field, errs in e.message_dict.items()]
            return JsonResponse({
                'success': False,
                'message': "Validation errors: " + "; ".join(errors)
            }, status=400)

        except Exception as e:
            logger.exception("Unexpected error saving academic info")
            return JsonResponse({
                'success': False,
                'message': "An unexpected error occurred. Please try again."
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    }, status=405)



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FinancialInfo, Registration
from django.core.exceptions import ValidationError

def save_financial_info(request):
    if request.method == 'POST':
        try:
            # Get user from session
            identity_card = request.session.get('identity_card')
            if not identity_card:
                return JsonResponse({
                    'success': False,
                    'locked': False,
                    'message': 'Session expired. Please log in again.'
                }, status=401)
                
            # Get user instance
            user = Registration.objects.get(identity_card=identity_card)
            if user.submission_date:
                return JsonResponse({
                    'success': False,
                    'locked': True,
                    'message': "Cannot update financial information after application submission."
                }, status=200)
            # Create or update financial info
            financial_info, created = FinancialInfo.objects.get_or_create(user=user)
            
            # Scholarship Information
            financial_info.scholarship_type = request.POST.get('scholarship_type')
            financial_info.referred_by_organization = request.POST.get('referred_by_organization') == 'Yes'
            financial_info.organization_name = request.POST.get('organization_name')
            
            # Scholarship Essays
            financial_info.why_sponsor_essay = request.POST.get('why_sponsor_essay')
            financial_info.future_impact_essay = request.POST.get('future_impact_essay')
            financial_info.suitable_candidate_essay = request.POST.get('suitable_candidate_essay')
            
            # Parent/Guardian 1 Information
            financial_info.parent1_marital_status = request.POST.get('parent1_marital_status')
            financial_info.parent1_name = request.POST.get('parent1_name')
            financial_info.parent1_identity_number = request.POST.get('parent1_identity_number')
            financial_info.parent1_nationality = request.POST.get('parent1_nationality')
            financial_info.parent1_phone = request.POST.get('parent1_phone')
            financial_info.parent1_relationship = request.POST.get('parent1_relationship')
            financial_info.parent1_occupation = request.POST.get('parent1_occupation')
            financial_info.parent1_salary_usd = request.POST.get('parent1_salary_usd')
            
            # Parent/Guardian 2 Information
            financial_info.parent2_marital_status = request.POST.get('parent2_marital_status')
            financial_info.parent2_name = request.POST.get('parent2_name')
            financial_info.parent2_identity_number = request.POST.get('parent2_identity_number')
            financial_info.parent2_nationality = request.POST.get('parent2_nationality')
            financial_info.parent2_phone = request.POST.get('parent2_phone')
            financial_info.parent2_relationship = request.POST.get('parent2_relationship')
            financial_info.parent2_occupation = request.POST.get('parent2_occupation')
            financial_info.parent2_salary_usd = request.POST.get('parent2_salary_usd')
            
            # Reference Information
            financial_info.referee1_name = request.POST.get('referee1_name')
            financial_info.referee1_relationship = request.POST.get('referee1_relationship')
            financial_info.referee1_phone = request.POST.get('referee1_phone')
            financial_info.referee1_email = request.POST.get('referee1_email')
            financial_info.referee1_address = request.POST.get('referee1_address')
            
            financial_info.referee2_name = request.POST.get('referee2_name')
            financial_info.referee2_relationship = request.POST.get('referee2_relationship')
            financial_info.referee2_phone = request.POST.get('referee2_phone')
            financial_info.referee2_email = request.POST.get('referee2_email')
            financial_info.referee2_address = request.POST.get('referee2_address')
            
            # Additional Information
            financial_info.has_relative_sponsored = request.POST.get('has_relative_sponsored') == 'Yes'
            financial_info.relative_details = request.POST.get('relative_details')
            
            # Validate and save
            financial_info.full_clean()
            financial_info.save()
            
            return JsonResponse({
                'success': True,
                'locked': False,
                'message': 'Financial information saved successfully!',
                'redirect_url': '/document-uploading/'
            })
            
        except Registration.DoesNotExist:
            return JsonResponse({
                'success': False,
                'locked': False,
                'message': 'User not found!'
            })
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'locked': False,
                'message': f'Validation error: {e}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'locked': False,
                'message': 'An error occurred while saving your information.'
            })
    
    # For GET request, render the form page
    return render(request, "bkend/financial-info.html")
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Registration, DocumentUpload
import os
from django.conf import settings

def save_documents(request):
    if request.method == 'POST':
        try:
            # Get user from session
            identity_card = request.session.get('identity_card')
            if not identity_card:
                return JsonResponse({
                    'success': False,
                    'locked': False,
                    'message': 'Session expired. Please log in again.'
                }, status=401)

            # Get user instance
            user = Registration.objects.get(identity_card=identity_card)
            
            # Check if the user has already submitted the application
            if user.submission_date:
                return JsonResponse({
                    'success': False,
                    'locked': True,
                    'message': "Cannot upload documents after application submission."
                }, status=200)

            # Create or update document upload record
            doc_upload, created = DocumentUpload.objects.get_or_create(user=user)
            
            # Handle file uploads
            def handle_upload(file_field_name, file_obj):
                if file_obj:
                    # Delete old file if exists
                    old_file = getattr(doc_upload, file_field_name)
                    if old_file:
                        old_file_path = os.path.join(settings.MEDIA_ROOT, str(old_file))
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    # Save new file
                    setattr(doc_upload, file_field_name, file_obj)

            # Required documents
            handle_upload('passport_mykad', request.FILES.get('passport_mykad'))
            handle_upload('high_school_certificate', request.FILES.get('high_school_certificate'))
            handle_upload('high_school_transcript', request.FILES.get('high_school_transcript'))
            handle_upload('highest_certificate', request.FILES.get('highest_certificate'))
            handle_upload('highest_transcript', request.FILES.get('highest_transcript'))
            
            # Optional documents
            handle_upload('english_proficiency', request.FILES.get('english_proficiency'))
            handle_upload('scholarship_letter', request.FILES.get('scholarship_letter'))
            handle_upload('father_passport', request.FILES.get('father_passport'))
            handle_upload('mother_passport', request.FILES.get('mother_passport'))
            handle_upload('father_income', request.FILES.get('father_income'))
            handle_upload('mother_income', request.FILES.get('mother_income'))
            handle_upload('utility_bill', request.FILES.get('utility_bill'))
            handle_upload('house_front_view', request.FILES.get('house_front_view'))
            handle_upload('kitchen_view', request.FILES.get('kitchen_view'))
            handle_upload('living_room_view', request.FILES.get('living_room_view'))
            handle_upload('referee_verification', request.FILES.get('referee_verification'))
            
            # Validate and save
            doc_upload.full_clean()
            doc_upload.save()

            return JsonResponse({
                'success': True,
                'locked': False,
                'message': 'Documents uploaded successfully!',
                'redirect_url': '/declaration-submission/'  # Include the URL for frontend redirection
            })
            
        except Registration.DoesNotExist:
            return JsonResponse({
                'success': False,
                'locked': False,
                'message': 'User not found!'
            })
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'locked': False,
                'message': f'Validation error: {e}'
            })
        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Error occurred in save_documents view: {str(e)}")
            return JsonResponse({
                'success': False,
                'locked': False,
                'message': f'An error occurred: {str(e)}'
            })
    
    # If not POST, redirect back to form
    return redirect('document-uploading')
from django.shortcuts import redirect
from django.contrib import messages
from .models import Registration
from django.utils import timezone
from django.views.decorators.http import require_POST

@require_POST
def submit_application(request):
    try:
        identity_card = request.session.get('identity_card')
        if not identity_card:
            return JsonResponse({
                'success': False,
                'message': 'Session expired. Please log in again.'
            }, status=401)
            
        user = Registration.objects.get(identity_card=identity_card)
        
        # If application already submitted, show a warning
        if user.application_submitted:
            return JsonResponse({
                'success': False,
                'message': 'Your application has already been submitted.'
            }, status=200)

        # Validate all required sections are complete
        validation_errors = []

        # 1. Check Basic Info
        try:
            basic_info = BasicInfo.objects.get(user=user)
            required_basic_fields = [
                'address', 'city', 'postcode',
                'country', 'gender', 'religion',
                'marital_status', 'birthdate',
                'country_of_birth', 'siblings_count',
                'nationality'
            ]
            for field in required_basic_fields:
                if not getattr(basic_info, field):
                    validation_errors.append(f"Basic Information: {field.replace('_', ' ')} is required")
        except BasicInfo.DoesNotExist:
            validation_errors.append("Basic Information section is incomplete")

        # 2. Check Academic Info
        try:
            academic_info = AcademicInfo.objects.get(user=user)
            required_academic_fields = [
                'high_school_name', 
                'high_school_level', 
                'highest_qualification',
                'cgpa_score'
            ]
            for field in required_academic_fields:
                if not getattr(academic_info, field):
                    validation_errors.append(f"Academic Information: {field.replace('_', ' ')} is required")
        except AcademicInfo.DoesNotExist:
            validation_errors.append("Academic Information section is incomplete")

        # 3. Check Financial Info
        try:
            financial_info = FinancialInfo.objects.get(user=user)
            required_financial_fields = [
                'why_sponsor_essay', 
                'future_impact_essay', 
                'suitable_candidate_essay',
                'parent1_name',
                'parent1_phone'
            ]
            for field in required_financial_fields:
                if not getattr(financial_info, field):
                    validation_errors.append(f"Financial Information: {field.replace('_', ' ')} is required")
        except FinancialInfo.DoesNotExist:
            validation_errors.append("Financial Information section is incomplete")

        # 4. Check Required Documents
        try:
            documents = DocumentUpload.objects.get(user=user)
            required_documents = [
                'passport_mykad', 
                'high_school_certificate',
                'high_school_transcript',
                'highest_certificate',
                'highest_transcript'
            ]
            for doc in required_documents:
                if not getattr(documents, doc):
                    validation_errors.append(f"Required document: {doc.replace('_', ' ')} is missing")
        except DocumentUpload.DoesNotExist:
            validation_errors.append("Document Upload section is incomplete")

        # If any validation errors exist, notify the user and redirect
        if validation_errors:
            error_message = "Cannot submit application. Please complete all required fields:"
            for error in validation_errors:
                error_message += f" - {error}"
            return JsonResponse({
                'success': False,
                'message': error_message
            }, status=400)

        # If no validation errors, mark as submitted
        user.application_submitted = True
        user.submission_date = timezone.now()
        user.save()

        # Success message upon successful submission
        return JsonResponse({
            'success': True,
            'message': 'Your application has been submitted successfully.',
            'redirect_url': '/view-status/'  # You can specify the URL you want to redirect to.
        })

    except Registration.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"An error occurred: {str(e)}"
        }, status=500)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Registration, ProgramSelection
from django.utils import timezone

def student_dashboard(request):
    """
    Main dashboard view that shows different options based on application state
    """
    # Check if user is logged in
    if not request.session.get('identity_card'):
        messages.error(request, "Please log in to access your dashboard")
        return redirect('login')
    
    try:
        # Get user and application status
        user = Registration.objects.get(identity_card=request.session['identity_card'])
        has_application = ProgramSelection.objects.filter(user=user).exists()
        is_submitted = user.application_submitted
        
        context = {
            'user': user,
            'existing_app': has_application,
            'submitted': is_submitted
        }
        return render(request, 'bkend/dashboard.html', context)
        
    except Registration.DoesNotExist:
        messages.error(request, "Please complete your registration first")
        return redirect('registration_form')
    except Exception as e:
        messages.error(request, f"System error: {str(e)}")
        return redirect('login')
from django.db import transaction

@require_POST
def delete_application(request):
    """
    Handles deletion of draft applications (only for non-submitted applications)
    Deletes all application-related data except Registration model
    """
    if not request.session.get('identity_card'):
        return redirect('login')
    
    try:
        user = Registration.objects.get(identity_card=request.session['identity_card'])
        
        # Prevent deletion if application is already submitted
        if user.application_submitted:
            messages.error(request, "Cannot delete a submitted application")
            return redirect('dashboard')
        
        # Delete all application-related data (except Registration)
        with transaction.atomic():
            # Delete program selection
            ProgramSelection.objects.filter(user=user).delete()
            
            # Delete basic info
            BasicInfo.objects.filter(user=user).delete()
            
            # Delete academic info (if you have this model)
            AcademicInfo.objects.filter(user=user).delete()
            
            # Delete financial info (if you have this model)
            FinancialInfo.objects.filter(user=user).delete()
            
            # Delete uploaded documents (if you have this model)
            DocumentUpload.objects.filter(user=user).delete()
            
            # Reset any submission flags
            user.application_submitted = False
            user.save()
            
            # Clear any relevant session data if needed
            if 'current_application_step' in request.session:
                del request.session['current_application_step']
        
        messages.success(request, "Draft application and all related data deleted successfully")
        return redirect('dashboard')
    
    except Registration.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')
    except Exception as e:
        messages.error(request, f"Error deleting application: {str(e)}")
        return redirect('dashboard')
        
    except Exception as e:
        messages.error(request, f"Error deleting application: {str(e)}")
    
    return redirect('dashboard')

def new_application(request):
    """
    Starts a new application only if no submitted application exists
    """
    if not request.session.get('identity_card'):
        return redirect('login')
    
    try:
        user = Registration.objects.get(identity_card=request.session['identity_card'])
        
        # Prevent new application if one is already submitted
        if user.application_submitted:
            messages.error(request, "You cannot create a new application while having a submitted application")
            return redirect('dashboard')
        
        # Clear any existing draft
        ProgramSelection.objects.filter(user=user).delete()
        BasicInfo.objects.filter(user=user).delete()
        AcademicInfo.objects.filter(user=user).delete()
        FinancialInfo.objects.filter(user=user).delete()
        DocumentUpload.objects.filter(user=user).delete()
        
        messages.info(request, "New application started")
        return redirect('program_selection')
        
    except Registration.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')
    except Exception as e:
        messages.error(request, f"Error starting new application: {str(e)}")
        return redirect('dashboard')

def view_status(request):
    """
    Shows application status page
    """
    if not request.session.get('identity_card'):
        return redirect('login')
    
    try:
        user = Registration.objects.get(identity_card=request.session['identity_card'])
        program = ProgramSelection.objects.filter(user=user).first()
        
        context = {
            'user': user,
            'program': program
        }
        return render(request, 'bkend/view-status.html', context)
        
    except Registration.DoesNotExist:
        messages.error(request, "No application found")
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, f"Error viewing status: {str(e)}")
        return redirect('dashboard')
from django.shortcuts import render
from bkend.models import Registration, ProgramSelection, BasicInfo, AcademicInfo, FinancialInfo, DocumentUpload
from django.db.models import Count, Q

from django.shortcuts import render
from bkend.models import Registration, ProgramSelection, BasicInfo, AcademicInfo, FinancialInfo, DocumentUpload
from django.db.models import Count, Q

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Registration

def staff_check(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(staff_check, login_url='admin_login')
def admin_dashboard(request):
    # Get counts for different application statuses
    status_counts = Registration.objects.aggregate(
        total=Count('identity_card'),
        submitted=Count('identity_card', filter=Q(application_submitted=True)),
        draft=Count('identity_card', filter=Q(application_submitted=False))
    )
    
    # Get recent submissions
    recent_submissions = Registration.objects.filter(
        application_submitted=True
    ).order_by('-submission_date')[:5]
    
    context = {
        'status_counts': status_counts,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'bkend/admin_dashboard.html', context)

from django.db.models import Q, F, Case, When, IntegerField
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Now
from django.shortcuts import render
from .models import Registration, BasicInfo, ProgramSelection, AcademicInfo
from datetime import date

from django.db.models import Q, Case, When, IntegerField
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Now
from datetime import date
from .models import Registration, BasicInfo, ProgramSelection
@login_required
@user_passes_test(staff_check, login_url='admin_login')
def admin_application_list(request, status='all'):
    # Base queryset with all necessary joins and annotations
    applications = Registration.objects.select_related(
        'basic_info',
        'academic_info',
        'financial_info'
    ).prefetch_related(
        'programselection_set'
    ).annotate(
        current_year=ExtractYear(Now()),
        current_month=ExtractMonth(Now()),
        current_day=ExtractDay(Now()),
        birth_year=ExtractYear(F('basic_info__birthdate')),
        birth_month=ExtractMonth(F('basic_info__birthdate')),
        birth_day=ExtractDay(F('basic_info__birthdate')),
        age=Case(
            When(
                Q(birth_month__lt=F('current_month')) |
                Q(birth_month=F('current_month'), birth_day__lte=F('current_day')),
                then=F('current_year') - F('birth_year')
            ),
            default=F('current_year') - F('birth_year') - 1,
            output_field=IntegerField()
        )
    ).distinct()  # Added distinct() to prevent duplicates from joins

    # Status filter - FIXED to use exact matches
    if status == 'submitted':
        applications = applications.filter(application_submitted=True)  # Use application_submitted field
        status_label = "Submitted Applications"
    elif status == 'draft':
        applications = applications.filter(application_submitted=False)  # Use application_submitted field
        status_label = "Draft Applications"
    else:
        status_label = "All Applications"

    # Search filter
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(identity_card__icontains=search_query) |
            Q(primary_email__icontains=search_query)
        )

    # Nationality filter
    nationality = request.GET.get('nationality')
    if nationality:
        applications = applications.filter(
            basic_info__nationality__iexact=nationality  # Changed to iexact for exact matching
        )

    # Gender filter
    gender = request.GET.get('gender')
    if gender:
        applications = applications.filter(
            basic_info__gender__iexact=gender
        )

    # Program filter - FIXED to use exact program matches
    program = request.GET.get('program')
    if program:
        applications = applications.filter(
            programselection__first_program__iexact=program  # Changed to iexact
        ).distinct()

    # Age range filter
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    if min_age:
        try:
            applications = applications.filter(age__gte=int(min_age))
        except ValueError:
            pass
    if max_age:
        try:
            applications = applications.filter(age__lte=int(max_age))
        except ValueError:
            pass

    # CGPA range filter
    min_cgpa = request.GET.get('min_cgpa')
    max_cgpa = request.GET.get('max_cgpa')
    if min_cgpa:
        try:
            applications = applications.filter(
                academic_info__cgpa_score__gte=float(min_cgpa)
            )
        except ValueError:
            pass
    if max_cgpa:
        try:
            applications = applications.filter(
                academic_info__cgpa_score__lte=float(max_cgpa)
            )
        except ValueError:
            pass

    # Date submitted range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        applications = applications.filter(submission_date__gte=date_from)
    if date_to:
        applications = applications.filter(submission_date__lte=date_to)

    # Ordering - with fallback to default ordering
    order_by = request.GET.get('order_by', '-submission_date')
    valid_ordering_fields = [
        'identity_card', 'first_name', 'primary_email', 
        'basic_info__nationality', 'academic_info__cgpa_score',
        'submission_date'
    ]
    
    if order_by.lstrip('-') in valid_ordering_fields:
        applications = applications.order_by(order_by)
    else:
        applications = applications.order_by('-submission_date')

    # Get distinct values for dropdowns
    gender_values = BasicInfo.objects.exclude(gender__isnull=True)\
                                   .order_by('gender')\
                                   .values_list('gender', flat=True)\
                                   .distinct()

    context = {
        'applications': applications,
        'status_label': status_label,
        'current_status': status,
        'today': date.today(),
        
        # Filter values
        'search_query': search_query,
        'nationality': nationality or '',
        'program': program or '',
        'gender': gender or '',
        'min_age': min_age or '',
        'max_age': max_age or '',
        'min_cgpa': min_cgpa or '',
        'max_cgpa': max_cgpa or '',
        'date_from': date_from or '',
        'date_to': date_to or '',
        'order_by': order_by,
        
        # Choices for dropdowns
        'gender_values': gender_values,
        'nationality_choices': BasicInfo.objects.exclude(nationality__isnull=True)
                                  .order_by('nationality')
                                  .values_list('nationality', flat=True)
                                  .distinct(),
        'program_choices': ProgramSelection.objects.exclude(first_program__isnull=True)
                              .order_by('first_program')
                              .values_list('first_program', flat=True)
                              .distinct(),
    }
    
    return render(request, 'bkend/admin_application_list.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
@login_required
@user_passes_test(staff_check, login_url='admin_login')
def admin_application_detail(request, identity_card):
    application = get_object_or_404(Registration, identity_card=identity_card)
    program_selection = ProgramSelection.objects.filter(user=application).first()
    basic_info = BasicInfo.objects.filter(user=application).first()
    academic_info = AcademicInfo.objects.filter(user=application).first()
    financial_info = FinancialInfo.objects.filter(user=application).first()
    documents = DocumentUpload.objects.filter(user=application).first()

    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')

        if action == 'shortlist':
            application.application_status = 'SHORTLISTED'
            application.shortlisted_date = timezone.now()
            #messages.success(request, 'Application marked as shortlisted for interview.')
        elif action == 'accept':
            application.application_status = 'ACCEPTED'
            application.accepted_date = timezone.now()
            #messages.success(request, 'Application marked as accepted.')
        elif action == 'reject':
            application.application_status = 'REJECTED'
            application.rejected_date = timezone.now()
            #messages.success(request, 'Application marked as rejected.')

        application.status_notes = notes
        application.save()
        return redirect('admin_application_detail', identity_card=identity_card)

    context = {
        'app': application,
        'program_selection': program_selection,
        'basic_info': basic_info,
        'academic_info': academic_info,
        'financial_info': financial_info,
        'documents': documents,
    }
    return render(request, 'bkend/admin_application_detail.html', context)
from django.views.generic import ListView
from .models import Registration

class ShortlistedApplicationsView(ListView):
    model = Registration
    template_name = 'bkend/shortlisted_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Registration.objects.filter(application_status='SHORTLISTED')
    


from django.http import HttpResponse
from django.views.generic import ListView
import csv
from django.http import HttpResponse
import csv
from django.utils import timezone
from django.utils.timesince import timesince


class AcceptedApplicationsView(ListView):
    model = Registration
    template_name = 'bkend/accepted_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        queryset = Registration.objects.filter(
            application_status='ACCEPTED'
        ).select_related(
            'basic_info', 'academic_info'
        ).prefetch_related(
            'programselection_set'
        )
        return queryset

    def get(self, request, *args, **kwargs):
        if 'download' in request.GET and request.GET['download'] == 'csv':
            return self.generate_csv()
        return super().get(request, *args, **kwargs)

    def generate_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="accepted_applications_{}.csv"'.format(
            timezone.now().strftime('%Y%m%d_%H%M')
        )

        writer = csv.writer(response)
        # Write headers
        writer.writerow([
            'ID', 'Name', 'Gender', 'Age', 'Email', 'Program',
            'Nationality', 'CGPA', 'Admission Status', 'Accepted Date'
        ])

        # Write data rows
        for app in self.get_queryset():
            program = app.programselection_set.first()
            
            # Calculate age
            age = ''
            if hasattr(app, 'basic_info') and app.basic_info.birthdate:
                age = timesince(app.basic_info.birthdate).split(',')[0]  # Gets the largest unit

            writer.writerow([
                app.identity_card,
                f"{app.first_name} {app.last_name}",
                app.basic_info.gender if hasattr(app, 'basic_info') and hasattr(app.basic_info, 'gender') else '',
                age,
                app.primary_email,
                program.first_program if program else '',
                app.basic_info.nationality if hasattr(app, 'basic_info') and hasattr(app.basic_info, 'nationality') else '',
                f"{app.academic_info.malaysian_equivalent:.2f}" if hasattr(app, 'academic_info') and app.academic_info.malaysian_equivalent else '',
                '',  # Empty Admission Status column
                app.accepted_date.strftime('%Y-%m-%d') if app.accepted_date else ''
            ])

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.db.models.functions import ExtractYear
from django.utils import timezone
from .models import Registration, ProgramSelection
from django.views.generic import TemplateView
from django.db.models import Count, Q
from .models import Registration, ProgramSelection  # Adjust based on your actual module path

class ApplicationStatisticsView(TemplateView):
    template_name = 'bkend/statistics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Registration.objects.all()
        
        # Status counts
        context['total_applications'] = int(queryset.count())
        context['accepted'] = int(queryset.filter(application_status='ACCEPTED').count())
        context['shortlisted'] = int(queryset.filter(application_status='SHORTLISTED').count())
        context['rejected'] = int(queryset.filter(application_status='REJECTED').count())
        context['ineligible'] = int(queryset.exclude(
            application_status__in=['ACCEPTED', 'SHORTLISTED', 'REJECTED']
        ).count())

        # Calculate acceptance rate
        total = context['total_applications']
        accepted = context['accepted']
        context['acceptance_rate'] = round((accepted / total) * 100, 2) if total > 0 else 0

        # Gender distribution by status
        context['gender_by_status'] = self.get_gender_by_status(queryset)

        # Top countries by status
        context['countries_by_status'] = self.get_countries_by_status(queryset)

        # Simplified program popularity
        context['program_popularity'] = self.get_simple_program_data()

        return context

    def get_gender_by_status(self, queryset):
        statuses = ['ACCEPTED', 'SHORTLISTED', 'REJECTED', 'OTHER']
        genders = ['Male', 'Female', 'Other']
        
        data = {status: [] for status in statuses}
        
        for status in statuses[:-1]:
            qs = queryset.filter(application_status=status)
            for gender in genders:
                count = qs.filter(basic_info__gender=gender).count()
                data[status].append({'gender': gender, 'count': int(count)})
        
        # For OTHER status
        qs = queryset.exclude(application_status__in=['ACCEPTED', 'SHORTLISTED', 'REJECTED'])
        for gender in genders:
            count = qs.filter(basic_info__gender=gender).count()
            data['OTHER'].append({'gender': gender, 'count': int(count)})
        
        return {
            'labels': genders,
            'datasets': [
                {
                    'label': 'Accepted',
                    'data': [item['count'] for item in data['ACCEPTED']],
                    'backgroundColor': '#28a745'
                },
                {
                    'label': 'Shortlisted',
                    'data': [item['count'] for item in data['SHORTLISTED']],
                    'backgroundColor': '#ffc107'
                },
                {
                    'label': 'Rejected',
                    'data': [item['count'] for item in data['REJECTED']],
                    'backgroundColor': '#dc3545'
                },
                {
                    'label': 'Other',
                    'data': [item['count'] for item in data['OTHER']],
                    'backgroundColor': '#6c757d'
                }
            ]
        }

    def get_countries_by_status(self, queryset):
        countries = (
            queryset.exclude(basic_info__nationality__isnull=True)
            .values('basic_info__nationality')
            .annotate(total=Count('identity_card'))
            .order_by('-total')[:10]
        )
        
        statuses = ['ACCEPTED', 'SHORTLISTED', 'REJECTED']
        data = []
        
        for country in countries:
            country_data = {'country': country['basic_info__nationality']}
            for status in statuses:
                count = queryset.filter(
                    basic_info__nationality=country['basic_info__nationality'],
                    application_status=status
                ).count()
                country_data[status.lower()] = int(count)
            data.append(country_data)
        
        return {
            'labels': [item['country'] for item in data],
            'datasets': [
                {
                    'label': 'Accepted',
                    'data': [item['accepted'] for item in data],
                    'backgroundColor': '#28a745'
                },
                {
                    'label': 'Shortlisted',
                    'data': [item['shortlisted'] for item in data],
                    'backgroundColor': '#ffc107'
                },
                {
                    'label': 'Rejected',
                    'data': [item['rejected'] for item in data],
                    'backgroundColor': '#dc3545'
                }
            ]
        }

    def get_simple_program_data(self):
        programs = (
            ProgramSelection.objects
            .values('first_program')
            .annotate(
                total=Count('user__identity_card'),
                accepted=Count('user__identity_card', filter=Q(user__application_status='ACCEPTED'))
            )
            .order_by('-total')[:10]
        )

        return {
            'labels': [p['first_program'] for p in programs],
            'datasets': [{
                'label': 'Applications',
                'data': [p['total'] for p in programs],
                'backgroundColor': '#007bff'
            }, {
                'label': 'Accepted',
                'data': [p['accepted'] for p in programs],
                'backgroundColor': '#28a745'
            }]
        }

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect

def admin_login(request):
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_dashboard')  # Make sure this matches your URL name
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:  # Check if user has admin privileges
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You don't have admin privileges.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'bkend/admin_login.html')  # Your login template

def admin_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('admin_login')  # Redirect to login page after logout

