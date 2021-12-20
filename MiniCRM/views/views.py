from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin

from MiniCRM.admin import UserChangeForm
from MiniCRM.filters import CompanyFilter
from MiniCRM.forms import CompanyOverallForm, ProjectOverallForm, PhoneCompanyInlineFormset, EmailCompanyInlineFormset, \
    MessageForm, MessageChangeForm, MessageSearchForm
from MiniCRM.models import Company, ProjectCompany, Message, User


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Checks the access permission and in case of its absence redirects the user to authentication.
        : return "login" url
    """
    login_url = reverse_lazy('login')

    def handle_no_permission(self) -> login_url:
        return redirect(self.get_login_url())


class CompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of company with ordering
    """

    permission_required = 'MiniCRM.can_see_companies'
    template_name = 'home.html'
    paginate_by = 2
    filterset_class = CompanyFilter

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


class CompanyCreateView(CreateView):
    """
    Displays a form for create a company
    """
    model = Company
    form_class = CompanyOverallForm
    template_name = 'company_create.html'
    permission_required = 'MiniCRM.change_company'

    def get(self, request, *args, **kwargs):
        self.object = None
        form = CompanyOverallForm(initial={'user': self.request.user},)
        phone_form = PhoneCompanyInlineFormset()
        email_form = EmailCompanyInlineFormset()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form))


class ProjectCompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of projects of company
    """
    model = ProjectCompany
    context_object_name = 'project_company_list'
    template_name = "company_projects.html"
    paginate_by = 2
    permission_required = 'MiniCRM.can_see_companies'


class ProjectCompanyDetailView(RedirectPermissionRequiredMixin, DetailView):
    """
    Generates a detail of project
    """

    model = ProjectCompany
    template_name = "project_detail.html"
    permission_required = 'MiniCRM.can_see_companies'

    def get_context_data(self, **kwargs):
        context = super(ProjectCompanyDetailView, self).get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(project=self.kwargs.get('pk')).order_by('-created')[:5]
        context['message_form'] = MessageForm()
        return context


class ProjectCompanyCreate(RedirectPermissionRequiredMixin, CreateView):
    """
    Implementation of the creation of a new project
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


class MessageCreateView(PermissionRequiredMixin, CreateView):
    """
    Implementation of the creation of a new message for project
    """
    model = Message
    form_class = MessageForm
    template_name = 'message.html'
    permission_required = 'MiniCRM.change_company'

    def get(self, request, *args, **kwargs):
        self.object = None
        form = MessageForm(initial={'manager': self.request.user, 'project': int(self.kwargs.get('pk'))},)
        return self.render_to_response(self.get_context_data(form=form))


class MessageDetailView(RedirectPermissionRequiredMixin, DetailView):
    """
    Generates a detail of message of project
    """

    model = Message
    template_name = "message_detail.html"
    permission_required = 'MiniCRM.change_company'


class MessageUpdateView(RedirectPermissionRequiredMixin, UpdateView):
    """
    Implementation of changes in information about the message of project.
    """
    model = Message
    form_class = MessageChangeForm
    template_name = 'message.html'
    permission_required = 'MiniCRM.change_company'


class MessageCompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of all messages of company projects
    """
    context_object_name = 'messages'
    template_name = "message_list_company.html"
    paginate_by = 5
    permission_required = 'MiniCRM.change_company'

    def get_queryset(self):
        """
        Get a filtered list of messages by user request (company id)
        :return: message list
        """
        company_id = self.kwargs.get('pk')  # getting pk from user request
        object_list = Message.objects.filter(project__company=company_id).order_by('-created')
        return object_list


class MessageProjectListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of messages of project
    """
    context_object_name = 'messages'
    template_name = "messages-project.html"
    paginate_by = 5
    permission_required = 'MiniCRM.change_company'

    def get_queryset(self):
        """
        Get a filtered list of messages by user request (project_id)
        :return: message list
        """
        project_id = self.kwargs.get('pk')  # getting pk from user request
        object_list = Message.objects.filter(project=project_id).order_by('-created')
        return object_list


class MessageListView(RedirectPermissionRequiredMixin, ListView):
    permission_required = 'MiniCRM.change_company'
    template_name = 'filter.html'
    paginate_by = 2
    form_class = MessageSearchForm
    context_object_name = 'object_list'

    def get_queryset(self, *args, **kwargs):
        queryset = Message.objects.filter(project=self.kwargs['pk']).order_by('-created')
        try:
            search_string = self.request.GET['search'].split()
            if search_string:
                for word in search_string:
                    queryset = queryset.filter(Q(message__icontains=word))
        except Exception:
            pass
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        form = MessageSearchForm()
        context['form'] = form
        return context


class PersonalArea(RedirectPermissionRequiredMixin, ListView):
    permission_required = 'MiniCRM.can_see_companies'
    template_name = 'profile.html'
    paginate_by = 2

    def get_queryset(self):
        try:
            personal_object = self.request.GET['personal_object']
            if personal_object == 'companies':
                companies = Company.objects.filter(user=self.request.user.pk).order_by('-date_created')
                return companies
            elif personal_object == 'projects':
                projects = ProjectCompany.objects.filter(user=self.request.user.pk).order_by('-created')
                return projects
            elif personal_object == 'comments':
                comments = Message.objects.filter(manager=self.request.user.pk).order_by('-created')
                return comments
        except Exception:
            return Company.objects.filter(user=self.request.user.pk).order_by('-date_created')


@login_required
def user_update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return reverse_lazy(request, 'profile.html')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'change_user.html', {"form": form})
