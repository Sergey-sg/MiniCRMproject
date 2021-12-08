from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View

from .forms import CompanyOverallForm, ProjectOverallForm, PhoneCompanyInlineFormset, EmailCompanyInlineFormset
from .models import Company, EmailCompany, PhoneCompany, ProjectCompany, CompanyLikes
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
    model = Company
    form_class = CompanyOverallForm
    template_name = 'company_update_form.html'
    permission_required = 'MiniCRM.change_company'

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone_form'] = PhoneCompanyInlineFormset(self.request.POST, instance=self.object)
            context['email_form'] = EmailCompanyInlineFormset(self.request.POST, instance=self.object)
        else:
            context['phone_form'] = PhoneCompanyInlineFormset(instance=self.object)
            context['email_form'] = EmailCompanyInlineFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        phone_form = context['phone_form']
        email_form = context['email_form']
        if phone_form.is_valid() and email_form.is_valid():
            self.object = form.save()
            phone_form.instance = self.object
            phone_form.save()
            email_form.instance = self.object
            email_form.save()
        return self.render_to_response(self.get_context_data(form=form))


class CompanyCreateView(CreateView):

    model = Company
    form_class = CompanyOverallForm
    template_name = 'company_create.html'
    permission_required = 'MiniCRM.change_company'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneCompanyInlineFormset()
        email_form = EmailCompanyInlineFormset()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneCompanyInlineFormset(self.request.POST)
        email_form = EmailCompanyInlineFormset(self.request.POST)
        if form.is_valid() and phone_form.is_valid() and email_form.is_valid():
            return self.form_valid(form, phone_form, email_form)
        else:
            return self.form_invalid(form, phone_form, email_form)

    def form_valid(self, form, phone_form, email_form):
        self.object = form.save()
        phone_form.instance = self.object
        phone_form.save()
        email_form.instance = self.object
        email_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, phone_form, email_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form))



# class CompanyCreateView(RedirectPermissionRequiredMixin, UpdateView):
#     model = Company
#     form_class = CompanyOverallForm
#     template_name = 'company_create.html'
#     permission_required = 'MiniCRM.change_company'
#
#     def get_success_url(self):
#         return reverse_lazy('company_detail', {self.model.pk})
#
#     def get_context_data(self, **kwargs):
#         context = super(CompanyCreateView, self).get_context_data(**kwargs)
#         context['phone_form'] = PhoneCompanyInlineFormset()
#         context['email_form'] = EmailCompanyInlineFormset()
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         phone_form = context['phone_form']
#         email_form = context['email_form']
#         if phone_form.is_valid() and email_form.is_valid():
#             self.object = form.save()
#             phone_form.instance = self.object
#             phone_form.save()
#             email_form.instance = self.object
#             email_form.save()
#         return self.render_to_response(self.get_context_data(form=form))

# def company_create(request):
#     """
#     This function creates a new Company object with related PhoneCompany and EmailCompany objects using inlineformset_factory
#     """
#
#     company = Company()
#     company_form = CompanyOverallForm(instance=company) # setup a form for the parent
#     phone_company_inline_form_set = PhoneCompanyInlineFormset
#     email_company_inline_form_set = EmailCompanyInlineFormset
#
#     if request.method == "POST":
#         company_form = CompanyOverallForm(request.POST)
#         formset_phone = phone_company_inline_form_set(request.POST)
#         formset_email = email_company_inline_form_set(request.POST)
#
#         if company_form.is_valid():
#             created_company = company_form.save(commit=False)
#             formset_phone = phone_company_inline_form_set(request.POST, instance=created_company)
#             formset_email = email_company_inline_form_set(request.POST, instance=created_company)
#
#             if formset_phone.is_valid() and formset_email.is_valid():
#                 created_company.save()
#                 formset_phone.save()
#                 formset_email.save()
#                 return HttpResponseRedirect(created_company.get_absolute_url())
#     else:
#         company_form = CompanyOverallForm(instance=company)
#         formset_phone = phone_company_inline_form_set()
#         formset_email = email_company_inline_form_set()
#
#     return render(request, 'company_create.html', {
#         'company_form': company_form,
#         'formset_phone': formset_phone,
#         'formset_email': formset_email
#     })





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


class AddLikeView(View):

    def post(self, request, *args, **kwargs):
        company_id = int(request.POST.get('company_id'))
        user_id = int(request.POST.get('user_id'))
        url_form = request.POST.get('url_form')

        user_inst = User.objects.get(id=user_id)
        company_inst = Company.objects.get(id=company_id)

        try:
            company_like_inst = CompanyLikes.objects.get(company=company_inst, liked_by=user_inst)
        except Exception as e:
            company_like = CompanyLikes(company=company_inst,
                                        liked_by=user_inst,
                                        like=True
                                        )
            company_like.save()

        return redirect(url_form)


class RemoveLikeView(View):

    def post(self, request, *args, **kwargs):
        company_likes_id = int(request.POST.get('company_likes_id'))
        url_form = request.POST.get('url_form')

        company_like = CompanyLikes.objects.get(id=company_likes_id)
        company_like.delete()

        return redirect(url_form)
