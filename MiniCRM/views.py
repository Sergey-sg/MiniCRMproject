from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View

from .filters import MessageFilter
from .forms import CompanyOverallForm, ProjectOverallForm, PhoneCompanyInlineFormset, EmailCompanyInlineFormset, \
    MessageForm
from .models import Company, EmailCompany, PhoneCompany, ProjectCompany, CompanyLikes, Message, MessageLike
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin


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
    Generates a list of companies, phones and emails
    """
    model = Company
    context_object_name = 'company_list'
    template_name = "home.html"
    queryset = Company.objects.all()
    paginate_by = 6
    permission_required = 'MiniCRM.can_see_companies'

    def get_context_data(self, **kwargs) -> dict:
        """adds phone and email lists to the context"""
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context.update({
            'phone_list': PhoneCompany.objects.all(),
            'email_list': EmailCompany.objects.all(),
        })
        return context

    def get_ordering(self) -> model:
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
        return HttpResponseRedirect(self.get_success_url())


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
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        form = CompanyOverallForm(initial={'user': self.request.user},)
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

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save()
        for arg in args:
            arg.instance = self.object
            arg.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=args[0],
                                  email_form=args[1]))


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


def personal_area(request):
    """
    Returns a link to the user's personal account
    :return "profile.html"
    """
    return render(request, 'profile.html')


class AddLikeView(View):
    """
    Adds likes of company.
    """

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
    """
    Remove likes of company
    """

    def post(self, request, *args, **kwargs):
        company_likes_id = int(request.POST.get('company_likes_id'))
        url_form = request.POST.get('url_form')

        company_like = CompanyLikes.objects.get(id=company_likes_id)
        company_like.delete()

        return redirect(url_form)


class AddMessageLikeView(View):
    """
    Adds likes to messages.
    """

    def post(self, request, *args, **kwargs):
        message_id = int(request.POST.get('message_id'))
        user_id = int(request.POST.get('user_id'))
        url_form = request.POST.get('url_form')

        user_inst = User.objects.get(id=user_id)
        message_inst = Message.objects.get(id=message_id)

        try:
            message_like_inst = MessageLike.objects.get(message=message_inst, liked_by=user_inst)
        except Exception as e:
            message_like = MessageLike(message=message_inst,
                                        liked_by=user_inst,
                                        like=True
                                        )
            message_like.save()

        return redirect(url_form)


class RemoveMessageLikeView(View):
    """
    Remove likes of messages
    """

    def post(self, request, *args, **kwargs):
        message_likes_id = int(request.POST.get('company_likes_id'))
        url_form = request.POST.get('url_form')

        message_like = MessageLike.objects.get(id=message_likes_id)
        message_like.delete()

        return redirect(url_form)


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

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, *args, **kwargs):
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
    form_class = MessageForm
    template_name = 'message.html'
    permission_required = 'MiniCRM.change_company'

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, *args, **kwargs):
        return self.render_to_response(self.get_context_data(form=form))


class MessageCompanyListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of all messages of company projects
    """
    model = Message
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
        object_list = self.model.objects.all().filter(project__company=company_id).order_by('-created')
        return object_list


class MessageProjectListView(RedirectPermissionRequiredMixin, ListView):
    """
    Generates a list of messages of project
    """
    model = Message
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
        object_list = self.model.objects.all().filter(project=project_id).order_by('-created')
        return object_list


def message_search(request, pk):
    f = MessageFilter(request.GET, queryset=Message.objects.filter(project=pk).order_by('-created'))
    paginator = Paginator(f.qs, 5)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return render(request, 'filter.html', {'filter': response, 'filter_form': f})
