from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, UpdateView

from MiniCRM.forms import CustomUserCreationForm, UserUpdateForm
from MiniCRM.models import User
from MiniCRM.views.views import RedirectPermissionRequiredMixin


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
    success_url = '/accounts/login/'

    def form_valid(self, form, **kwargs):
        object_form = form.save()
        group = Group.objects.get(name='user')
        object_form.groups.add(group)
        object_form.save()
        return super(UserCreateView, self).form_valid(form)
