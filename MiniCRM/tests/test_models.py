from django.test import TestCase
from ..models import Company, PhoneCompany, EmailCompany, ProjectCompany


class CompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Company.objects.create(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
            )

    def test_name_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('name').max_length
        self.assertEquals(max_length, 300)

    def test_description_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_position_person_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('position_person').verbose_name
        self.assertEquals(field_label, 'position person')

    def test_position_person_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('position_person').max_length
        self.assertEquals(max_length, 300)

    def test_contact_person_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('contact_person').verbose_name
        self.assertEquals(field_label, 'contact person')

    def test_contact_person_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('contact_person').max_length
        self.assertEquals(max_length, 450)

    def test_address_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_address_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('address').max_length
        self.assertEquals(max_length, 250)

    def test_company_name_is_name(self):
        company = Company.objects.get(id=1)
        expected_object_name = company.name
        self.assertEquals(expected_object_name, str(company))


class PhoneCompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
            )
        company.save()
        # Set up non-modified objects used by all test methods
        PhoneCompany.objects.create(phone_number='+380564562345', company=company)

    def test_phone_label(self):
        phone = PhoneCompany.objects.get(id=1)
        field_phone = phone._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_phone, 'phone number')

    def test_phone_max_length(self):
        phone = PhoneCompany.objects.get(id=1)
        max_length = phone._meta.get_field('phone_number').max_length
        self.assertEquals(max_length, 13)

    def test_company_is_company(self):
        phone = PhoneCompany.objects.get(id=1)
        field_company = phone.company
        self.assertTrue(type(field_company) is Company)

    def test_phone_str_is_phone(self):
        phone = PhoneCompany.objects.get(id=1)
        expected_phone_company = phone.phone_number
        self.assertEquals(expected_phone_company, str(phone))


class EmailCompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
            )
        company.save()
        # Set up non-modified objects used by all test methods
        EmailCompany.objects.create(email='fdfgsg@gmail.com', company=company)

    def test_email_label(self):
        email = EmailCompany.objects.get(id=1)
        field_email = email._meta.get_field('email').verbose_name
        self.assertEquals(field_email, 'email')

    def test_phone_max_length(self):
        email = EmailCompany.objects.get(id=1)
        max_length = email._meta.get_field('email').max_length
        self.assertEquals(max_length, 254)

    def test_company_is_company(self):
        email = EmailCompany.objects.get(id=1)
        field_company = email.company
        self.assertTrue(type(field_company) is Company)

    def test_email_str_is_email(self):
        email = EmailCompany.objects.get(id=1)
        expected_email_company = email.email
        self.assertEquals(expected_email_company, str(email))


class ProjectCompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
            )
        company.save()
        # Set up non-modified objects used by all test methods
        ProjectCompany.objects.create(
            company=company,
            name='project test',
            description="Project description",
            start_dates='2021-12-20',
            deadline='2021-12-25',
            price='240',
            )

    def test_company_is_company(self):
        project = ProjectCompany.objects.get(id=1)
        field_company = project.company
        self.assertTrue(type(field_company) is Company)

    def test_name_label(self):
        project = ProjectCompany.objects.get(id=1)
        field_label = project._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        project = ProjectCompany.objects.get(id=1)
        max_length = project._meta.get_field('name').max_length
        self.assertEquals(max_length, 300)

    def test_description_label(self):
        project = ProjectCompany.objects.get(id=1)
        field_label = project._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_start_dates_label(self):
        project = ProjectCompany.objects.get(id=1)
        field_label = project._meta.get_field('start_dates').verbose_name
        self.assertEquals(field_label, 'start dates')

    def test_deadline_label(self):
        project = ProjectCompany.objects.get(id=1)
        field_label = project._meta.get_field('deadline').verbose_name
        self.assertEquals(field_label, 'deadline')

    def test_price_label(self):
        project = ProjectCompany.objects.get(id=1)
        field_label = project._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')

    def test_price_max_length(self):
        project = ProjectCompany.objects.get(id=1)
        max_digits = project._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 10)

    def test_company_name_is_name(self):
        project = ProjectCompany.objects.get(id=1)
        expected_object_name = project.name
        self.assertEquals(expected_object_name, str(project))
