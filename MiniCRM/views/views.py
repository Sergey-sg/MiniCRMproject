from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin

from MiniCRM.forms import ProjectCreateForm, MessageForm, UserUpdateForm, CustomUserCreationForm
from MiniCRM.models import Company, ProjectCompany, Message, User


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Checks the access permission and in case of its absence redirects the user to authentication.
        : return "login" url
    """
    login_url = reverse_lazy('login')

    def handle_no_permission(self) -> login_url:
        return redirect(self.get_login_url())


class ProjectCompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of projects of company
    """
    model = ProjectCompany
    context_object_name = 'project_company_list'
    template_name = "company_projects.html"
    paginate_by = 2
    permission_required = 'MiniCRM.can_see_companies'


class ProjectCompanyCreate(RedirectPermissionRequiredMixin, CreateView):
    """
    Implementation of the creation of a new project
    """
    model = ProjectCompany
    form_class = ProjectCreateForm
    template_name = 'project_create.html'
    permission_required = 'MiniCRM.change_company'

    def form_valid(self, form):
        object_form = form.save(commit=False)
        object_form.user = self.request.user
        object_form.save()
        return super(ProjectCompanyCreate, self).form_valid(form)


class ProjectCompanyUpdateView(RedirectPermissionRequiredMixin, UpdateView):
    """
    Implementation of changes in information about the project.
    """
    model = ProjectCompany
    form_class = ProjectCreateForm
    template_name = 'project_update.html'
    permission_required = 'MiniCRM.change_company'

    def get_queryset(self, *args, **kwargs):
        queryset = super(ProjectCompanyUpdateView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class MessageCreateView(RedirectPermissionRequiredMixin, CreateView):
    """
    Implementation of the creation of a new message for project
    """
    model = Message
    form_class = MessageForm
    template_name = 'message.html'
    permission_required = 'MiniCRM.change_company'

    def form_valid(self, form, **kwargs):
        object_form = form.save(commit=False)
        object_form.manager = self.request.user
        object_form.project = ProjectCompany.objects.get(pk=self.kwargs.get('pk'))
        object_form.save()
        return super(MessageCreateView, self).form_valid(form)


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
    form_class = MessageForm
    template_name = 'message.html'
    permission_required = 'MiniCRM.change_company'

    def get_queryset(self, *args, **kwargs):
        queryset = super(MessageUpdateView, self).get_queryset()
        return queryset.filter(manager=self.request.user)


class ProjectWithMessageListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of messages for project and send to context
        'message_form' - form for created new message
    """
    permission_required = 'MiniCRM.change_company'
    template_name = 'project_detail_with_comments.html'
    paginate_by = 2
    context_object_name = 'object_list'

    def get_queryset(self, *args, **kwargs):
        """filter messages with input-search"""
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
        context = super(ProjectWithMessageListView, self).get_context_data(**kwargs)
        context['message_form'] = MessageForm() # called in project_detail_with_comments.html with action='message_created'
        context['project'] = ProjectCompany.objects.get(pk=self.kwargs['pk'])
        return context


class PersonalArea(RedirectPermissionRequiredMixin, ListView):
    """
    Send to 'profile.html' companies, messages, projects which are user-created
    """
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


class UserChangeView(RedirectPermissionRequiredMixin, UpdateView):
    """
    Custom user change for users
    """
    permission_required = 'MiniCRM.can_see_companies'
    template_name = 'change_user.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        user = self.request.user.pk
        return User.objects.get(pk=user)

    def get_success_url(self):
        return '/accounts/profile/'


class MyPasswordChangeView(RedirectPermissionRequiredMixin, PasswordChangeView):
    """
    Custom password change for users
    """
    permission_required = 'MiniCRM.can_see_companies'
    template_name = 'password_change.html'
    form_class = PasswordChangeForm

    def get_object(self, queryset=None):
        user = self.request.user.pk
        return User.objects.get(pk=user)

    def get_success_url(self):
        return '/accounts/profile/'


class CustomLoginView(LoginView):

    def get_context_data(self, *args, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context['create_user_form'] = CustomUserCreationForm()
        return context


class UserCreateView(CreateView):
    model = User
    template_name = '../templates/registration/create_user.html'
    form_class = CustomUserCreationForm
    success_url = '/accounts/change/'

    def form_valid(self, form, **kwargs):
        object_form = form.save()
        group = Group.objects.get(name='user')
        object_form.groups.add(group)
        object_form.save()
        return super(UserCreateView, self).form_valid(form)
