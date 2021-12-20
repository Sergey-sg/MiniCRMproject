from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserCreationForm, UserChangeForm
from .models import Company, EmailCompany, PhoneCompany, ProjectCompany, CompanyLikes, Message, Communication, \
    CompanyDisLike, User


class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', ]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'groups', 'user_permissions', 'is_staff',
                           'is_active', 'user_photo')}),
        )


admin.site.register(Company)
admin.site.register(PhoneCompany)
admin.site.register(EmailCompany)
admin.site.register(ProjectCompany)
admin.site.register(CompanyLikes)
admin.site.register(CompanyDisLike)
admin.site.register(Message)
admin.site.register(Communication)
admin.site.register(User, CustomUserAdmin)
