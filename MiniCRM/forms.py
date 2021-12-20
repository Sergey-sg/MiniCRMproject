from ckeditor.fields import RichTextField
from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChange
from django.forms import fields, inlineformset_factory

from .models import Company, ProjectCompany, PhoneCompany, EmailCompany, Message, User


class CompanyOverallForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'


PhoneCompanyInlineFormset = inlineformset_factory(
    Company,
    PhoneCompany,
    fields=('phone_number', ),
    extra=2,
    can_delete=False,
)

EmailCompanyInlineFormset = inlineformset_factory(
    Company,
    EmailCompany,
    fields=('email', ),
    extra=2,
    can_delete=False,
)


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


class MessageForm(forms.ModelForm):
    """
    Form for creat message of project.
    """
    class Meta:
        model = Message
        fields = '__all__'


class MessageChangeForm(forms.ModelForm):
    """
    Form for creat message of project.
    """
    class Meta:
        model = Message
        fields = ('message', 'communication_options')


class MessageSearchForm(forms.ModelForm):
    search = forms.TextInput()

    class Meta:
        model = Message
        fields = ('message',)


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
