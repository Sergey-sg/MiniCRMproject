from django.test import TestCase

from ..forms import ProjectOverallForm, CompanyOverallForm


class ProjectOverallFormTest(TestCase):

    def test_name_form_label(self):
        form = ProjectOverallForm()
        self.assertTrue(
            form.fields['name'].label == None or form.fields['name'].label == 'name')

    def test_description_form_label(self):
        form = ProjectOverallForm()
        self.assertEquals(
            form.fields['description'].label, None or 'Description')

    def test_description_help_text(self):
        form = ProjectOverallForm()
        self.assertEqual(form.fields['description'].help_text, 'Project description')

    def test_start_dates_form_label(self):
        form = ProjectOverallForm()
        self.assertTrue(
            form.fields['start_dates'].label == None or form.fields['start_dates'].label == 'start_dates')

    def test_deadline_form_label(self):
        form = ProjectOverallForm()
        self.assertTrue(
            form.fields['deadline'].label == None or form.fields['deadline'].label == 'deadline')

    def test_deadline_form_date_in_past(self):
        start_date = '2021-12-21'
        deadline = '2021-12-20'
        form_data = {'start_dates': start_date, 'deadline': deadline}
        form = ProjectOverallForm(data=form_data)
        self.assertFalse(form.is_valid())
