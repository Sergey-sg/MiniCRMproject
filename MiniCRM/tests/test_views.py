from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from ..forms import PhoneCompanyInlineFormset, EmailCompanyInlineFormset, CompanyCreateForm
from ..models import Company, User


class CompanyListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 3 companies for pagination tests
        number_of_companies = 3
        for company_num in range(number_of_companies):
            Company.objects.create(
                name=f'test company {company_num}',
                description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
                position_person='manager',
                contact_person=f'g dfg ggg {company_num}',
                address=f'gdfdf gdfgdgd gdgdggd {company_num}',
                )
        permission1 = Permission.objects.get(codename='change_company')
        permission2 = Permission.objects.get(codename='can_see_companies')
        group = Group.objects.create(name='manager')
        group.permissions.add(permission1, permission2)
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.groups.add(group)
        user.save()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_not_login(self):
        resp = self.client.get('')
        self.assertEqual(resp.url, '/accounts/login/')

    def test_view_url_accessible_by_name(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(reverse_lazy('home'))
        self.assertTemplateUsed(resp, 'home.html')

    def test_pagination_is_two(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(reverse('home'))
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['company_list']) == 2)

    def test_lists_all_companies(self):
        self.client.login(username='john', password='johnpassword')
        # Get second page and confirm it has (exactly) remaining 1 items
        resp = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['company_list']) == 1)


class CompanyDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 3 companies for pagination tests
        number_of_companies = 3
        for company_num in range(number_of_companies):
            Company.objects.create(
                name=f'test company {company_num}',
                description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh",
                position_person='manager',
                contact_person=f'g dfg ggg {company_num}',
                address=f'gdfdf gdfgdgd gdgdggd {company_num}',
            )
        permission1 = Permission.objects.get(codename='change_company')
        permission2 = Permission.objects.get(codename='can_see_companies')
        group = Group.objects.create(name='manager')
        group.permissions.add(permission1, permission2)
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.groups.add(group)
        user.save()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get('/company/1/detail/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get(reverse('company_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get('/company/1/detail/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'company_detail.html')


class CompanyUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 3 companies for pagination tests
        number_of_companies = 3
        permission1 = Permission.objects.get(codename='change_company')
        permission2 = Permission.objects.get(codename='can_see_companies')
        group = Group.objects.create(name='manager')
        group.permissions.add(permission1, permission2)
        for company_num in range(number_of_companies):
            user = User.objects.create_user(f'john{company_num}', f'lennon{company_num}@thebeatles.com', 'johnpassword')
            user.groups.add(group)
            user.save()
            Company.objects.create(
                name=f'test company {company_num}',
                description="description",
                position_person='manager',
                contact_person=f'contact_person {company_num}',
                address=f'address {company_num}',
                user=user
                )

    def test_company_update_queryset(self):
        self.client.login(username='john0', password='johnpassword')
        resp = self.client.get('/company/2/update/')
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get('/company/1/update/')
        self.assertEqual(resp.status_code, 200)

    def test_company_update_context_data(self):
        self.client.login(username='john0', password='johnpassword')
        resp = self.client.get('/company/1/update/')
        self.assertEqual(type(resp.context['phone_form']), PhoneCompanyInlineFormset)
        self.assertEqual(type(resp.context['email_form']), EmailCompanyInlineFormset)

    def test_not_login(self):
        resp = self.client.get('')
        self.assertEqual(resp.url, '/accounts/login/')


class CompanyCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 3 companies for pagination tests
        permission1 = Permission.objects.get(codename='change_company')
        permission2 = Permission.objects.get(codename='can_see_companies')
        group = Group.objects.create(name='manager')
        group.permissions.add(permission1, permission2)
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.groups.add(group)
        user.save()
        # Company.objects.create(
        #     name='test company',
        #     description="description",
        #     position_person='manager',
        #     contact_person='contact_person',
        #     address='address',
        #     user=user
        #     )

    def test_company_get(self):
        self.client.login(username='john', password='johnpassword')
        resp = self.client.get('/company/create/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(type(resp.context['form']), CompanyCreateForm)
        self.assertEqual(type(resp.context['phone_form']), PhoneCompanyInlineFormset)
        self.assertEqual(type(resp.context['email_form']), EmailCompanyInlineFormset)

    # def test_company_post(self):
    #     self.client.login(username='john', password='johnpassword')
    #     resp = self.client.get('/company/create/')
    #     form_data = dict(
    #             name='test company',
    #             description="description",
    #             position_person='manager',
    #             contact_person='contact_person',
    #             address='address',
    #     )
    #     form = CompanyCreateForm(data=form_data)
    #     # phone = resp.context['phone_form']
    #     # email = resp.context['email_form']
    #     # phone['phone_number'] = '+380454564545'
    #     # email['email'] = 'ew@er.rft'
    #     self.assertTrue(form.is_valid())

    def test_post_create_company_view_POST_success(self):
        data = dict(
                name='test company',
                description="description",
                position_person='manager',
                contact_person='contact_person',
                address='address',
        )
        self.client.login(username='john', password='johnpassword')
        # resp = self.client.get('/company/create/')
        resp = self.client.post('/company/create/', data=data, follow=True)
        # response = self.client.post(self.add_post_url, data=data,
        #                             follow=True)  # make sure your url is correct too btw that could also be the issue
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(Company.objects.get(pk=1), resp.user)


    # def test_company_update_context_data(self):
    #     self.client.login(username='john0', password='johnpassword')
    #     resp = self.client.get('/company/1/update/')
    #     self.assertEqual(type(resp.context['phone_form']), PhoneCompanyInlineFormset)
    #     self.assertEqual(type(resp.context['email_form']), EmailCompanyInlineFormset)

    def test_not_login(self):
        resp = self.client.get('')
        self.assertEqual(resp.url, '/accounts/login/')

