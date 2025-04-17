# forms.py
from django import forms

class ShortlistEmailForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Email subject'}),
        initial="Congratulations! Your Application Has Been Shortlisted"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'Email message'}),
        initial="""Dear {full_name},

We are pleased to inform you that your application for {program} has been shortlisted.

[Additional instructions or information]

Best regards,
[Your Name]
[Your Organization]"""
    )