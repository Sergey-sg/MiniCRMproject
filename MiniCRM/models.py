from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse


class Company(models.Model):
    """
    Company model
attributes:
     name (str): company name;
     description (str): Description of the company
     date_created (datetime): Date the entry was created (added automatically)
     date_modified (datetime): Date the entry was last modified
     contact_person (str): Full name of the contact person
     position_person (str): Position of the contact person
     address (str): Company address
    """
    name = models.CharField(max_length=300)
    description = RichTextField(blank=True, null=True, help_text="Company description")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    contact_person = models.CharField(max_length=450, help_text="Full name of the contact person")
    position_person = models.CharField(max_length=300, help_text="Position of the contact person")
    address = models.CharField(max_length=250, blank=True, help_text="Company address")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='add_company', null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('company_detail', args=[str(self.id)])

    def __str__(self):
        """class method returns the company name in string representation"""
        return self.name

    class Meta:
        permissions = (("can_see_companies", "Can see companies"),)


class PhoneCompany(models.Model):
    """
        Phone numbers model
    attributes:
         phone_regex (value): RegexValidator of phone number
         phone_number (str): phone number of company
         company (class Company): communication with the Company
    """
    phone_regex = RegexValidator(regex=r'^\+380\d{9}',
                                 message='Phone number must be in format: "+380999999999". Up to "+380" and 9 digits.')
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True,
                                    help_text='Phone number must be in format: "+380999999999"')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        """class method returns the phone number of company in string representation"""
        return self.phone_number


class EmailCompany(models.Model):
    """
        Phone numbers model
    attributes:
        email (str): email of company
        company (class Company): communication with the Company
    """
    email = models.EmailField(max_length=254,)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        """class method returns the email of company in string representation"""
        return self.email


class ProjectCompany(models.Model):
    """
    Project of company model
        attributes:
             company (class Company): communication with the Company
             name (str): name project
             description (str): project description
             start_dates (datetime): the date of start project
             deadline (datetime): the date of deadline
             price (int): price project
    """
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=300)
    description = RichTextField(blank=True, null=True, help_text="Project description")
    start_dates = models.DateField(null=True, blank=True, help_text="Enter the date of start project")
    deadline = models.DateField(null=True, blank=True, help_text="Enter the date of deadline")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter price project")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='add_project', on_delete=models.CASCADE)

    def clean_fields(self, exclude=None):
        """
        checking the validity of the project end date
        """
        if self.deadline:
            if self.start_dates > self.deadline:
                raise ValidationError('The project cannot end before it starts.')
        return self.start_dates

    def get_absolute_url(self):
        """
        Returns the url to access a particular project instance.
        """
        return reverse('project_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='add_message', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectCompany, on_delete=models.CASCADE)
    message = RichTextField()
    created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='add_like', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True)
    like = models.BooleanField('Like', default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message}: {self.user} - {self.like}'


class InteractionInformationCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectCompany, on_delete=models.CASCADE)
    manager_interaction = models.CharField(max_length=100)
    # likes = GenericRelation(Like)

    @property
    def total_likes(self):
        return self.likes.count()


# class Tweet(models.Model):
#     body = models.CharField(max_length=140)
#     likes = GenericRelation(Like)
#     def __str__(self):
#         return self.body
#     @property
#     def total_likes(self):
#         return self.likes.count()


# Канала обращения (Заявка; Письмо; Сайт; Инициатива компании)
# Оценка (можно лайк / дизлайк или оценки от -5 до 5 или др)