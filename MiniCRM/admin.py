from django.contrib import admin
from .models import Company, EmailCompany, PhoneCompany, ProjectCompany, CompanyLikes, Message, \
    InteractionInformationCompany, Communication, CompanyDisLike

admin.site.register(Company)
admin.site.register(PhoneCompany)
admin.site.register(EmailCompany)
admin.site.register(ProjectCompany)
admin.site.register(CompanyLikes)
admin.site.register(CompanyDisLike)
admin.site.register(Message)
admin.site.register(InteractionInformationCompany)
admin.site.register(Communication)
