from django.db import models

# Registration model
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import os

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import os

class Registration(models.Model):
    
    APPLICATION_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('SHORTLISTED', 'Shortlisted for Interview'),
        ('REJECTED', 'Rejected'),
        ('ACCEPTED', 'Accepted'),
    ]
    identity_card = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    primary_email = models.EmailField(unique=True)
    secondary_email = models.EmailField(blank=True, null=True)
    country_code = models.CharField(max_length=5)
    contact_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)  # Hashed password
    applicant_type = models.CharField(max_length=50)
    application_submitted = models.BooleanField(default=False)
    submission_date = models.DateTimeField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/default.jpg'
    )
    application_status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='DRAFT'
    )
    shortlisted_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)
    accepted_date = models.DateTimeField(null=True, blank=True)
    status_notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.identity_card})"
    
    def set_password(self, raw_password):
        """Hashes and sets the password."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifies the password."""
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        """Hashes password before saving (skips file checks)."""
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.set_password(self.password)
        super().save(*args, **kwargs)
# Program Selection model
class ProgramSelection(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE)  # Link to Registration
    first_program = models.CharField(max_length=255)
    second_program = models.CharField(max_length=255, blank=True, null=True)
    third_program = models.CharField(max_length=255, blank=True, null=True)
    fourth_program = models.CharField(max_length=255, blank=True, null=True)
    intake_year = models.CharField(max_length=50)
    study_mode = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.primary_email} - {self.first_program}"
    
from django.db import models
from .models import Registration  # Import your existing Registration model

class BasicInfo(models.Model):
    # Relationship to Registration (one-to-one)
    user = models.OneToOneField(
        Registration, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='basic_info'
    )
    
    # Personal Details
    address = models.TextField()
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    religion = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20)
    birthdate = models.DateField()
    country_of_birth = models.CharField(max_length=100)
    siblings_count = models.PositiveIntegerField()
    nationality = models.CharField(max_length=100)
    skype_account = models.CharField(max_length=100, blank=True, null=True)
    
    # Personal Statement
    transferring_institution = models.BooleanField(default=False)
    disability_info = models.TextField(blank=True, null=True)
    allergies_info = models.TextField(blank=True, null=True)
    
    # Passport Details
    passport_issue_date = models.DateField()
    passport_issue_place = models.CharField(max_length=100)
    has_malaysian_pass = models.BooleanField(default=False)
    passport_expiry_date = models.DateField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Basic Info for {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Basic Information"
        verbose_name_plural = "Basic Information Records"
    
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Registration  # Import your Registration model

class AcademicInfo(models.Model):
    # ======================
    # 1. Model Relationships
    # ======================
    user = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='academic_info'
    )
    
    # ======================
    # 2. High School Qualification
    # ======================
    HIGH_SCHOOL_LEVEL_CHOICES = [
        ('GRADE_10', 'High School Grade 10'),
        ('O_LEVEL', 'O Level'),
    ]
    high_school_level = models.CharField(
        max_length=50,
        choices=HIGH_SCHOOL_LEVEL_CHOICES,
        blank=True,
        null=True
    )
    high_school_name = models.CharField(max_length=255, blank=True, null=True)
    high_school_address = models.TextField(blank=True, null=True)
    high_school_country = models.CharField(max_length=100, blank=True, null=True)
    english_score = models.CharField(max_length=50, blank=True, null=True)
    math_score = models.CharField(max_length=50, blank=True, null=True)
    
    # ======================
    # 3. Highest Academic Qualification
    # ======================
    HIGHEST_QUALIFICATION_CHOICES = [
        ('MATRICULATION', 'Matriculation'),
        ('GRADE_12', 'High School Grade 12'),
        ('A_LEVEL', 'A-Level'),
        ('DIPLOMA', 'Diploma'),
        ('STAM', 'Sijil Tinggi Agama Malaysia (STAM)'),
        ('STPM', 'Sijil Tinggi Persekolahan Malaysia (STPM)'),
    ]
    highest_qualification = models.CharField(
        max_length=50,
        choices=HIGHEST_QUALIFICATION_CHOICES,
        blank=True,
        null=True
    )
    program_name = models.CharField(max_length=255, blank=True, null=True)
    
    # CGPA Fields with Validation
    cgpa_score = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Original CGPA/Score from your institution"
    )
    cgpa_scale = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.1)],  # Prevent division by zero
        help_text="Maximum possible CGPA/Score (e.g., 4.0, 5.0, 10.0)"
    )
    malaysian_equivalent = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(4.0)],
        help_text="Automatically calculated Malaysian equivalent CGPA (scale 4.0)",
        db_index=True  # For faster filtering
    )
    
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    
    # ======================
    # 4. English Proficiency
    # ======================
    LANGUAGE_CHOICES = [
        ('ENGLISH', 'English'),
        ('NON_ENGLISH', 'Non-English'),
    ]
    national_language = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES,
        blank=True,
        null=True
    )
    
    ENGLISH_TEST_CHOICES = [
        ('IELTS', 'IELTS'),
        ('TOEFL', 'TOEFL'),
        ('LINGUASKILL', 'Linguaskill'),
        ('MUET', 'MUET'),
        ('OTHER', 'Others'),
    ]
    english_test_type = models.CharField(
        max_length=50,
        choices=ENGLISH_TEST_CHOICES,
        blank=True,
        null=True
    )
    test_year = models.CharField(max_length=4, blank=True, null=True)
    band_score = models.CharField(max_length=50, blank=True, null=True)
    
    # ======================
    # 5. Timestamps & Metadata
    # ======================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Academic Information"
        verbose_name_plural = "Academic Information Records"
        indexes = [
            models.Index(fields=['malaysian_equivalent']),
            models.Index(fields=['highest_qualification']),
        ]
        ordering = ['-malaysian_equivalent']  # Default ordering by CGPA
    
    def __str__(self):
        return f"Academic Info for {self.user.first_name} {self.user.last_name} (CGPA: {self.malaysian_equivalent or 'N/A'})"
    
    def calculate_malaysian_cgpa(self):
        """
        Calculate the Malaysian equivalent CGPA on a 4.0 scale
        Returns None if calculation isn't possible
        """
        if None in (self.cgpa_score, self.cgpa_scale) or self.cgpa_scale == 0:
            return None
        
        raw_value = (self.cgpa_score / self.cgpa_scale) * 4.0
        return min(4.0, round(raw_value, 2))  # Cap at 4.0 and round
    
    def save(self, *args, **kwargs):
        """Auto-calculate Malaysian CGPA before saving"""
        self.malaysian_equivalent = self.calculate_malaysian_cgpa()
        super().save(*args, **kwargs)
    
    def get_cgpa_display(self):
        """Formatted CGPA information for display"""
        if self.malaysian_equivalent is not None:
            return f"{self.malaysian_equivalent}/4.0 (Original: {self.cgpa_score}/{self.cgpa_scale})"
        return "Not available"

class FinancialInfo(models.Model):
    # Relationship to Registration (one-to-one)
    user = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='financial_info'
    )
    
    # Scholarship Information
    SCHOLARSHIP_TYPE_CHOICES = [
        ('FULL', 'Full Scholarship'),
        ('PARTIAL_TUITION', 'Partial Scholarship - Tuition Fee Only'),
        ('PARTIAL_TUITION_ACCOMMODATION', 'Partial Scholarship - Tuition Fee and Accommodation'),
        ('PARTIAL_TUITION_ALLOWANCE', 'Partial Scholarship - Tuition Fee and Monthly Allowance'),
    ]
    scholarship_type = models.CharField(
        max_length=50,
        choices=SCHOLARSHIP_TYPE_CHOICES,
        blank=True,
        null=True
    )
    
    referred_by_organization = models.BooleanField(default=False)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Scholarship Essays
    why_sponsor_essay = models.TextField(blank=True, null=True)
    future_impact_essay = models.TextField(blank=True, null=True)
    suitable_candidate_essay = models.TextField(blank=True, null=True)
    
    # Parent/Guardian 1 Information
    parent1_marital_status = models.CharField(max_length=20, blank=True, null=True)
    parent1_name = models.CharField(max_length=255, blank=True, null=True)
    parent1_identity_number = models.CharField(max_length=50, blank=True, null=True)
    parent1_nationality = models.CharField(max_length=100, blank=True, null=True)
    parent1_phone = models.CharField(max_length=20, blank=True, null=True)
    parent1_relationship = models.CharField(max_length=50, blank=True, null=True)
    parent1_occupation = models.CharField(max_length=100, blank=True, null=True)
    parent1_salary_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    
    # Parent/Guardian 2 Information
    parent2_marital_status = models.CharField(max_length=20, blank=True, null=True)
    parent2_name = models.CharField(max_length=255, blank=True, null=True)
    parent2_identity_number = models.CharField(max_length=50, blank=True, null=True)
    parent2_nationality = models.CharField(max_length=100, blank=True, null=True)
    parent2_phone = models.CharField(max_length=20, blank=True, null=True)
    parent2_relationship = models.CharField(max_length=50, blank=True, null=True)
    parent2_occupation = models.CharField(max_length=100, blank=True, null=True)
    parent2_salary_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    
    # Reference Information
    referee1_name = models.CharField(max_length=255, blank=True, null=True)
    referee1_relationship = models.CharField(max_length=100, blank=True, null=True)
    referee1_phone = models.CharField(max_length=20, blank=True, null=True)
    referee1_email = models.EmailField(blank=True, null=True)
    referee1_address = models.TextField(blank=True, null=True)
    
    referee2_name = models.CharField(max_length=255, blank=True, null=True)
    referee2_relationship = models.CharField(max_length=100, blank=True, null=True)
    referee2_phone = models.CharField(max_length=20, blank=True, null=True)
    referee2_email = models.EmailField(blank=True, null=True)
    referee2_address = models.TextField(blank=True, null=True)
    
    # Additional Information
    has_relative_sponsored = models.BooleanField(default=False)
    relative_details = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Financial Info for {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Financial Information"
        verbose_name_plural = "Financial Information Records"

class DocumentUpload(models.Model):
    # Relationship to Registration (one-to-one)
    user = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='documents'
    )
    
    # Required Documents (temporarily set to optional)
    passport_mykad = models.FileField(upload_to='documents/passport_mykad/', 
                                    blank=True, null=True,
                                    verbose_name="Passport/MYKAD")
    high_school_certificate = models.FileField(upload_to='documents/high_school/', 
                                             blank=True, null=True,
                                             verbose_name="High School Certificate")
    high_school_transcript = models.FileField(upload_to='documents/high_school/', 
                                            blank=True, null=True,
                                            verbose_name="High School Transcript")
    highest_certificate = models.FileField(upload_to='documents/highest_education/', 
                                         blank=True, null=True,
                                         verbose_name="Highest Academic Certificate")
    highest_transcript = models.FileField(upload_to='documents/highest_education/', 
                                        blank=True, null=True,
                                        verbose_name="Highest Academic Transcript")
    
    # Optional Documents
    english_proficiency = models.FileField(upload_to='documents/english_proficiency/', 
                                         blank=True, null=True, 
                                         verbose_name="English Proficiency")
    scholarship_letter = models.FileField(upload_to='documents/scholarship/', 
                                        blank=True, null=True, 
                                        verbose_name="Scholarship Letter")
    father_passport = models.FileField(upload_to='documents/parent_docs/', 
                                     blank=True, null=True, 
                                     verbose_name="Father's Passport/Death Certificate")
    mother_passport = models.FileField(upload_to='documents/parent_docs/', 
                                     blank=True, null=True, 
                                     verbose_name="Mother's Passport/Death Certificate")
    father_income = models.FileField(upload_to='documents/income/', 
                                   blank=True, null=True, 
                                   verbose_name="Father's Income Slip")
    mother_income = models.FileField(upload_to='documents/income/', 
                                   blank=True, null=True, 
                                   verbose_name="Mother's Income Slip")
    utility_bill = models.FileField(upload_to='documents/utility/', 
                                  blank=True, null=True, 
                                  verbose_name="Utility Bill")
    referee_verification = models.FileField(upload_to='documents/referee/', 
                                          blank=True, null=True, 
                                          verbose_name="Referee Verification Letter")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Documents for {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Document Upload"
        verbose_name_plural = "Document Uploads"