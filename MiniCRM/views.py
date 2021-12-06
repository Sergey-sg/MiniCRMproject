from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CompanyOverallForm, ProjectOverallForm
from .models import Company, EmailCompany, PhoneCompany, ProjectCompany
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        return redirect(self.get_login_url())


class CompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of companies, phones and emails
    """
    model = Company
    context_object_name = 'company_list'
    template_name = "home.html"
    queryset = Company.objects.all()
    paginate_by = 2
    permission_required = 'MiniCRM.can_see_companies'

    def get_context_data(self, **kwargs):
        """adds phone and email lists to the context"""
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context.update({
            'phone_list': PhoneCompany.objects.all(),
            'email_list': EmailCompany.objects.all(),
        })
        return context

    def get_ordering(self):
        """sorting implementation method"""
        ordering = self.request.GET.get('orderby')
        return ordering


class CompanyDetailView(RedirectPermissionRequiredMixin, DetailView):
    """
    Generates a detail of company
    """

    model = Company
    template_name = "company_detail.html"
    permission_required = 'MiniCRM.can_see_companies'

    def get_context_data(self, **kwargs):
        """adds phone and email lists to the context"""
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context.update({
            'phone_list': PhoneCompany.objects.all(),
            'email_list': EmailCompany.objects.all(),
        })
        return context


class CompanyUpdateView(RedirectPermissionRequiredMixin, UpdateView):
    """
    Implementation of changes in information about the company
    """
    model = Company
    form_class = CompanyOverallForm
    template_name = 'company_update_form.html'
    permission_required = 'MiniCRM.change_company'

    def form_valid(self, form):
        super(CompanyUpdateView, self).form_valid(form)
        company = form.instance
        phone_company = company.phonecompany_set.first()
        phone_company.phone_number = form.cleaned_data.get('phone_number')
        # phone_company.phone_number = form.fields()
        phone_company.save()
        email_company = company.emailcompany_set.first()
        email_company.email = form.cleaned_data.get('email')
        email_company.save()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))


class CompanyCreate(RedirectPermissionRequiredMixin, CreateView):
    """
    Implementation of the creation of a new company
    """
    model = Company
    # form_class = CompanyOverallForm
    fields = '__all__'
    template_name = 'company_create.html'
    permission_required = 'MiniCRM.change_company'

    def form_valid(self, form):
        super(CompanyCreate, self).form_valid(form)
        company = form.instance
        phone_company = company.phonecompany_set.first()
        phone_company.phone_number = form.phone_number.get('phone_number')
        phone_company.save()
        email_company = company.emailcompany_set
        email_company.email = form.email.get('email')
        email_company.save()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))


class ProjectCompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of projects of company
    """
    model = ProjectCompany
    context_object_name = 'project_company_list'
    template_name = "company_projects.html"
    paginate_by = 6
    permission_required = 'MiniCRM.can_see_companies'

    def get_queryset(self):
        """
        Get a filtered list of projects by user request (company id)
        :return: project list for company
        """
        company_id = self.kwargs.get('pk')    # getting pk from user request
        object_list = self.model.objects.all().filter(company_id=company_id)
        return object_list

    def get_ordering(self):
        """sorting implementation method"""
        ordering = self.request.GET.get('orderby')
        return ordering


class ProjectCompanyDetailView(RedirectPermissionRequiredMixin, DetailView):
    """
    Generates a detail of project
    """

    model = ProjectCompany
    template_name = "project_detail.html"
    permission_required = 'MiniCRM.can_see_companies'


class ProjectCompanyCreate(RedirectPermissionRequiredMixin, CreateView):
    """
    Implementation of the creation of a new company
    """
    model = ProjectCompany
    form_class = ProjectOverallForm
    template_name = 'project_create.html'
    permission_required = 'MiniCRM.change_company'


class ProjectCompanyUpdateView(RedirectPermissionRequiredMixin, UpdateView):
    """
    Implementation of changes in information about the project.
    """
    model = ProjectCompany
    form_class = ProjectOverallForm
    template_name = 'project_update.html'
    permission_required = 'MiniCRM.change_company'


def personal_area(request):
    return render(request, 'profile.html')

# def like_comment(request, comment):
#     if request.session.get('has_commented', False):
#         return HttpResponse("You've already commented.")
#     c = comments.Comment(comment=new_comment)
#     c.save()
#     request.session['has_commented'] = True
#     return HttpResponse('Thanks for your comment!')