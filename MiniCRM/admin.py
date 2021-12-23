from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserCreationForm, UserChangeForm
from .models import Company, EmailCompany, PhoneCompany, ProjectCompany, CompanyLikes, Message, Communication, \
    CompanyDisLike, User, MessageLike, MessageDisLike


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', ]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'groups', 'user_permissions', 'is_staff',
                           'is_active', 'user_photo')}),
        )


@admin.register(PhoneCompany)
class PhoneCompanyAdmin(admin.ModelAdmin):
    list_display = ("company", "phone_number")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("project", "manager", "communication_options", )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "date_created", "contact_person", "user", )


@admin.register(CompanyDisLike)
class CompanyDisLikeAdmin(admin.ModelAdmin):
    list_display = ("company", "disliked_by", "created", "dislike", )


@admin.register(EmailCompany)
class EmailCompanyAdmin(admin.ModelAdmin):
    list_display = ("company", "email")


@admin.register(CompanyLikes)
class CompanyLikesAdmin(admin.ModelAdmin):
    list_display = ("company", "liked_by", "created", "like", )


@admin.register(ProjectCompany)
class ProjectCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "start_dates", "deadline", "price", "user", )


@admin.register(MessageLike)
class MessageLikeAdmin(admin.ModelAdmin):
    list_display = ("message", "liked_by", "created", "like", )


@admin.register(MessageDisLike)
class MessageDisLikeAdmin(admin.ModelAdmin):
    list_display = ("message", "disliked_by", "created", "dislike", )


admin.site.register(Communication)
