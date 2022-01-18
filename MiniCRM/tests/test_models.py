from django.contrib.auth.models import Permission, Group
from django.test import TestCase
from ..models import Company, PhoneCompany, EmailCompany, ProjectCompany, User, Communication, Message, MessageLike, \
    MessageDisLike, CompanyLikes, CompanyDisLike


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()

    def test_default_user_photo(self):
        user = User.objects.get(id=1)
        field_photo = user.user_photo.name
        self.assertEquals(field_photo, 'default_user_photo.png')

    def test_user_str_is_username(self):
        user = User.objects.get(id=1)
        expected_object_name = user.username
        self.assertEquals(expected_object_name, str(user))


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

    def test_company_absolute_url(self):
        company = Company.objects.get(id=1)
        self.assertEquals(company.get_absolute_url(), '/company/1/detail/')


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

    def test_email_max_length(self):
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

    def test_project_str_is_project(self):
        project = ProjectCompany.objects.get(id=1)
        expected_object_name = project.name
        self.assertEquals(expected_object_name, str(project))

    def test_project_absolute_url(self):
        project = ProjectCompany.objects.get(id=1)
        self.assertEquals(project.get_absolute_url(), '/project/1/detail/')


class CommunicationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        communication = Communication.objects.create(communication='test communication')
        communication.save()

    def test_name_label(self):
        communication = Communication.objects.get(id=1)
        field_label = communication._meta.get_field('communication').verbose_name
        self.assertEquals(field_label, 'communication')

    def test_name_max_length(self):
        communication = Communication.objects.get(id=1)
        max_length = communication._meta.get_field('communication').max_length
        self.assertEquals(max_length, 50)

    def test_project_str_is_project(self):
        communication = Communication.objects.get(id=1)
        expected_object_name = communication.communication
        self.assertEquals(expected_object_name, str(communication))


class MessageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        company = Company.objects.create(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
        )
        company.save()
        project = ProjectCompany.objects.create(
            company=company,
            name='project test',
            description="Project description",
            start_dates='2021-12-20',
            deadline='2021-12-25',
            price='240',
        )
        project.save()
        communication = Communication.objects.create(communication='test communication')
        communication.save()
        message = Message.objects.create(
            manager=user,
            project=project,
            message='bla-bla-bla',
            communication_options=communication,
            )
        message.save()

    def test_name_label(self):
        project = ProjectCompany.objects.get(id=1)
        field_label = project._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_project_is_project(self):
        message = Message.objects.get(id=1)
        field_project = message.project
        self.assertTrue(type(field_project) is ProjectCompany)

    def test_manager_is_user(self):
        message = Message.objects.get(id=1)
        field_manager = message.manager
        self.assertTrue(type(field_manager) is User)

    def test_communication_options_is_communication(self):
        message = Message.objects.get(id=1)
        field_communication = message.communication_options
        self.assertTrue(type(field_communication) is Communication)

    def test_message_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_project_str_is_project(self):
        message = Message.objects.get(id=1)
        expected_object_name = f'{message.manager}--{message.project}--{message.created}'
        self.assertEquals(expected_object_name, str(message))

    def test_message_absolute_url(self):
        message = Message.objects.get(id=1)
        self.assertEquals(message.get_absolute_url(), '/project/message/1/detail/')


class MessageLikeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        company = Company.objects.create(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
        )
        company.save()
        project = ProjectCompany.objects.create(
            company=company,
            name='project test',
            description="Project description",
            start_dates='2021-12-20',
            deadline='2021-12-25',
            price='240',
        )
        project.save()
        communication = Communication.objects.create(communication='test communication')
        communication.save()
        message = Message.objects.create(
            manager=user,
            project=project,
            message='bla-bla-bla',
            communication_options=communication,
        )
        message.save()
        message_like = MessageLike.objects.create(
            liked_by=user,
            message=message,
            like=True,
            )
        message_like.save()

    def test_liked_by_is_user(self):
        like = MessageLike.objects.get(id=1)
        field_liked_by = like.liked_by
        self.assertTrue(type(field_liked_by) is User)

    def test_liked_by_label(self):
        like = MessageLike.objects.get(id=1)
        field_label = like._meta.get_field('liked_by').verbose_name
        self.assertEquals(field_label, 'liked by')

    def test_message_is_message(self):
        like = MessageLike.objects.get(id=1)
        field_message = like.message
        self.assertTrue(type(field_message) is Message)

    def test_message_label(self):
        like = MessageLike.objects.get(id=1)
        field_label = like._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_like(self):
        like = MessageLike.objects.get(id=1)
        field_like = like.like
        self.assertTrue(field_like)

    def test_like_label(self):
        like = MessageLike.objects.get(id=1)
        field_label = like._meta.get_field('like').verbose_name
        self.assertEquals(field_label, 'Like')

    def test_like_str_is_like(self):
        like = MessageLike.objects.get(id=1)
        expected_object_name = f'{like.message}: {like.liked_by} - {like.like}'
        self.assertEquals(expected_object_name, str(like))

class MessageDisLikeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        company = Company.objects.create(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
        )
        company.save()
        project = ProjectCompany.objects.create(
            company=company,
            name='project test',
            description="Project description",
            start_dates='2021-12-20',
            deadline='2021-12-25',
            price='240',
        )
        project.save()
        communication = Communication.objects.create(communication='test communication')
        communication.save()
        message = Message.objects.create(
            manager=user,
            project=project,
            message='bla-bla-bla',
            communication_options=communication,
        )
        message.save()
        message_dislike = MessageDisLike.objects.create(
            disliked_by=user,
            message=message,
            dislike=True,
            )
        message_dislike.save()

    def test_disliked_by_is_user(self):
        dislike = MessageDisLike.objects.get(id=1)
        field_disliked_by = dislike.disliked_by
        self.assertTrue(type(field_disliked_by) is User)

    def test_disliked_by_label(self):
        dislike = MessageDisLike.objects.get(id=1)
        field_label = dislike._meta.get_field('disliked_by').verbose_name
        self.assertEquals(field_label, 'disliked by')

    def test_message_is_message(self):
        dislike = MessageDisLike.objects.get(id=1)
        field_message = dislike.message
        self.assertTrue(type(field_message) is Message)

    def test_message_label(self):
        dislike = MessageDisLike.objects.get(id=1)
        field_label = dislike._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_dislike(self):
        dislike = MessageDisLike.objects.get(id=1)
        field_dislike = dislike.dislike
        self.assertTrue(field_dislike)

    def test_dislike_label(self):
        dislike = MessageDisLike.objects.get(id=1)
        field_label = dislike._meta.get_field('dislike').verbose_name
        self.assertEquals(field_label, 'DisLike')

    def test_dislike_str_is_like(self):
        dislike = MessageDisLike.objects.get(id=1)
        expected_object_name = f'{dislike.message}: {dislike.disliked_by} - {dislike.dislike} - {dislike.created}'
        self.assertEquals(expected_object_name, str(dislike))


class CompanyLikesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        company = Company.objects.create(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
        )
        company.save()
        company_like = CompanyLikes.objects.create(
            liked_by=user,
            company=company,
            like=True,
            )
        company_like.save()

    def test_liked_by_is_user(self):
        like = CompanyLikes.objects.get(id=1)
        field_liked_by = like.liked_by
        self.assertTrue(type(field_liked_by) is User)

    def test_liked_by_label(self):
        like = CompanyLikes.objects.get(id=1)
        field_label = like._meta.get_field('liked_by').verbose_name
        self.assertEquals(field_label, 'liked by')

    def test_company_is_company(self):
        like = CompanyLikes.objects.get(id=1)
        field_company = like.company
        self.assertTrue(type(field_company) is Company)

    def test_company_label(self):
        like = CompanyLikes.objects.get(id=1)
        field_label = like._meta.get_field('company').verbose_name
        self.assertEquals(field_label, 'company')

    def test_like(self):
        like = CompanyLikes.objects.get(id=1)
        field_like = like.like
        self.assertTrue(field_like)

    def test_like_label(self):
        like = CompanyLikes.objects.get(id=1)
        field_label = like._meta.get_field('like').verbose_name
        self.assertEquals(field_label, 'Like')

    def test_like_str_is_like(self):
        like = CompanyLikes.objects.get(id=1)
        expected_object_name = f'{like.company}: {like.liked_by} - {like.like}'
        self.assertEquals(expected_object_name, str(like))


class CompanyDisLikeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        company = Company.objects.create(
            name='test company',
            description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
            position_person='manager',
            contact_person='fg dfg ggg',
            address='gdfdf gdfgdgd gdgdggd',
        )
        company.save()
        company_dislike = CompanyDisLike.objects.create(
            disliked_by=user,
            company=company,
            dislike=True,
            )
        company_dislike.save()

    def test_disliked_by_is_user(self):
        dislike = CompanyDisLike.objects.get(id=1)
        field_disliked_by = dislike.disliked_by
        self.assertTrue(type(field_disliked_by) is User)

    def test_disliked_by_label(self):
        dislike = CompanyDisLike.objects.get(id=1)
        field_label = dislike._meta.get_field('disliked_by').verbose_name
        self.assertEquals(field_label, 'disliked by')

    def test_company_is_company(self):
        dislike = CompanyDisLike.objects.get(id=1)
        field_company = dislike.company
        self.assertTrue(type(field_company) is Company)

    def test_company_label(self):
        dislike = CompanyDisLike.objects.get(id=1)
        field_label = dislike._meta.get_field('company').verbose_name
        self.assertEquals(field_label, 'company')

    def test_dislike(self):
        dislike = CompanyDisLike.objects.get(id=1)
        field_dislike = dislike.dislike
        self.assertTrue(field_dislike)

    def test_dislike_label(self):
        dislike = CompanyDisLike.objects.get(id=1)
        field_label = dislike._meta.get_field('dislike').verbose_name
        self.assertEquals(field_label, 'DisLike')

    def test_dislike_str_is_dislike(self):
        dislike = CompanyDisLike.objects.get(id=1)
        expected_object_name = f'{dislike.company}: {dislike.disliked_by} - {dislike.dislike} - {dislike.created}'
        self.assertEquals(expected_object_name, str(dislike))
