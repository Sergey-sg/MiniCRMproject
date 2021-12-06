from ckeditor.fields import RichTextField
from django import forms
from django.core.validators import RegexValidator
from django.forms import fields

from .models import Company, ProjectCompany


class CompanyOverallForm(forms.ModelForm):
    """
    Form for editing information about the company.
        attributes:
             name (str): company name
             description (str): Description of the company
             date_created (datetime): Date the entry was created (added automatically)
             date_modified (datetime): Date the entry was last modified
             contact_person (str): Full name of the contact person
             position_person (str): Position of the contact person
             address (str): Company address
             phone_regex: regex validator for phone number
             phone_number (str): phone number of company
             email (url): email of company
    """
    name = forms.CharField(max_length=300)
    description = RichTextField(blank=True, null=True, help_text="Company description")
    contact_person = forms.CharField(max_length=450, help_text="Full name of the contact person")
    position_person = forms.CharField(max_length=300, help_text="Position of the contact person")
    address = forms.CharField(max_length=250, help_text="Company address")
    phone_regex = RegexValidator(regex=r'^\+380\d{9}')
    phone_number = forms.CharField(validators=[phone_regex],
                                   max_length=13,
                                   error_messages={'required': 'Phone number must be in format: "+380999999999". Up to "+380" and 9 digits.'},
                                   help_text='Phone number must be in format: "+380999999999"')
    email = forms.EmailField(max_length=254,)

    class Meta:
        model = Company
        fields = '__all__'


class ProjectOverallForm(forms.ModelForm):
    """
    Form for editing information about the project.
        attributes:
            name (str): name project
            description (str): project description
            start_dates (datetime): the date of start project
            deadline (datetime): the date of deadline
            price (int): price project
    """
    name = forms.CharField(max_length=300)
    description = RichTextField(blank=True, null=True, help_text="Project description")
    start_dates = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), help_text="Enter the date of start project")
    deadline = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), help_text="Enter the date of deadline")
    price = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = ProjectCompany
        fields = '__all__'
