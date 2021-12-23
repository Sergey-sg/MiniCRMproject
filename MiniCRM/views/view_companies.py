from django.views.generic import CreateView, UpdateView
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from MiniCRM.filters import CompanyFilter
from MiniCRM.forms import CompanyCreateForm, PhoneCompanyInlineFormset, EmailCompanyInlineFormset, MessageForm,\
    MessageSearchForm
from MiniCRM.models import Company, Message
from MiniCRM.views.views import RedirectPermissionRequiredMixin


class CompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of company with ordering
    """
    permission_required = 'MiniCRM.can_see_companies'
    template_name = 'home.html'
    paginate_by = 2
    filterset_class = CompanyFilter
    model = Company

    def get_queryset(self):
        """Return the filtered queryset"""
        queryset = Company.objects.all()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        """Add to context filter as "filterset" """
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CompanyDetailView(RedirectPermissionRequiredMixin, DetailView):
    """
    Generates a detail of company
    """
    model = Company
    template_name = "company_detail.html"
    permission_required = 'MiniCRM.can_see_companies'


class CompanyUpdateView(RedirectPermissionRequiredMixin, UpdateView):
    """
    Displays a form for editing information about a company.
    """
    model = Company
    form_class = CompanyCreateForm
    template_name = 'company_update_form.html'
    permission_required = 'MiniCRM.change_company'

    def get_queryset(self, *args, **kwargs):
        queryset = super(CompanyUpdateView, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone_form'] = PhoneCompanyInlineFormset(self.request.POST, instance=self.object)
            context['email_form'] = EmailCompanyInlineFormset(self.request.POST, instance=self.object)
        else:
            context['phone_form'] = PhoneCompanyInlineFormset(instance=self.object)
            context['email_form'] = EmailCompanyInlineFormset(instance=self.object)
        return context


class CompanyCreateView(RedirectPermissionRequiredMixin, CreateView):
    """
    Displays a form for create a company
    """
    model = Company
    form_class = CompanyCreateForm
    template_name = 'company_create.html'
    permission_required = 'MiniCRM.change_company'

    def get_context_data(self, **kwargs):
        form = CompanyCreateForm()
        phone_form = PhoneCompanyInlineFormset()
        email_form = EmailCompanyInlineFormset()
        return {'form': form, 'phone_form': phone_form, 'email_form': email_form}

    def form_valid(self, form):
        object_form = form.save(commit=False)
        object_form.user = self.request.user
        return super(CompanyCreateView, self).form_valid(form)


class MessageCompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of all messages of company projects
    """
    form_class = MessageSearchForm
    context_object_name = 'object_list'
    template_name = "messages_company.html"
    paginate_by = 5
    permission_required = 'MiniCRM.change_company'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('pk')  # getting pk from user request
        queryset = Message.objects.filter(project__company=company_id).order_by('-created')
        try:
            search_string = self.request.GET['search'].split()
            if search_string:
                for word in search_string:
                    queryset = queryset.filter(Q(message__icontains=word))
        except Exception:
            pass
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MessageCompanyListView, self).get_context_data(**kwargs)
        form = MessageSearchForm()
        context['form'] = form
        context['message_form'] = MessageForm()
        return context
