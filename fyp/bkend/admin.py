from django.contrib import admin
from .models import Registration, ProgramSelection, BasicInfo, AcademicInfo, FinancialInfo, DocumentUpload, PrescreeningCriteria, Country
from django.db.utils import IntegrityError
import pycountry

# Register the Registration model
admin.site.register(Registration)

# Register the ProgramSelection model
admin.site.register(ProgramSelection)

# Register the BasicInfo model
admin.site.register(BasicInfo)
admin.site.register(AcademicInfo)
admin.site.register(FinancialInfo)

# Load countries dynamically into the Country model
def load_countries():
    from .models import Country
    for country in pycountry.countries:
        try:
            Country.objects.get_or_create(name=country.name)
        except IntegrityError:
            pass  # Skip duplicates

# Call the function to load countries
load_countries()

from django.contrib import admin
from django.utils.html import format_html
from .models import DocumentUpload

# Unregister first if already registered
if DocumentUpload in admin.site._registry:
    admin.site.unregister(DocumentUpload)

@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_links')
    readonly_fields = ('document_links',)
    search_fields = ('user__first_name', 'user__last_name', 'user__identity_card')
    
    def document_links(self, obj):
        doc_fields = [
            ('passport_mykad', 'Passport/MYKAD'),
            ('high_school_certificate', 'High School Cert'),
            ('high_school_transcript', 'High School Transcript'),
            ('highest_certificate', 'Highest Cert'),
            ('highest_transcript', 'Highest Transcript'),
            ('english_proficiency', 'English Proficiency'),
            ('scholarship_letter', 'Scholarship Letter'),
            ('father_passport', "Father's Passport"),
            ('mother_passport', "Mother's Passport"),
            ('father_income', "Father's Income"),
            ('mother_income', "Mother's Income"),
            ('utility_bill', 'Utility Bill'),
            ('referee_verification', 'Referee Letter')
        ]
        
        links = []
        for field, display_name in doc_fields:
            file = getattr(obj, field)
            if file:
                links.append(
                    f'<strong>{display_name}:</strong> '
                    f'<a href="{file.url}" target="_blank">View</a> | '
                    f'<a href="/admin/bkend/documentupload/{obj.pk}/change/#id_{field}">Change</a>'
                )
        
        return format_html('<br>'.join(links)) if links else "No documents"
    
    document_links.short_description = "Uploaded Documents"

@admin.register(PrescreeningCriteria)
class PrescreeningCriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'minimum_cgpa', 'minimum_age', 'maximum_age','gender','marital_status')  # Include maximum_age
    filter_horizontal = ('countries', 'ineligible_countries')  # Enable dropdowns for ManyToMany fields
    search_fields = ('name',)
    list_filter = ('minimum_cgpa', 'minimum_age', 'maximum_age', 'marital_status')  # Add maximum_age to filters

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

