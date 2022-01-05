from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChange, UserCreationForm
from django.forms import fields, inlineformset_factory

from .models import Company, ProjectCompany, PhoneCompany, EmailCompany, Message, User


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'description', 'contact_person', 'position_person', 'address')


PhoneCompanyInlineFormset = inlineformset_factory(
    Company,
    PhoneCompany,
    fields=('phone_number', ),
    extra=2,
    can_delete_extra=False,
)

EmailCompanyInlineFormset = inlineformset_factory(
    Company,
    EmailCompany,
    fields=('email', ),
    extra=2,
    can_delete_extra=False,
)


class ProjectCreateForm(forms.ModelForm):
    """
    Form for editing information about the project.
        attributes:
            start_dates (datetime): the date of start project
            deadline (datetime): the date of deadline
    """
    start_dates = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), help_text="Enter the date of start project")
    deadline = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), help_text="Enter the date of deadline")

    class Meta:
        model = ProjectCompany
        exclude = ('user', )


class MessageForm(forms.ModelForm):
    """
    Form for creat message of project.
    """
    class Meta:
        model = Message
        fields = ('message', 'communication_options', )


class UserUpdateForm(UserChange):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_photo', 'email', 'password')


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'user_photo', )
