from django.contrib import admin
from .models import Company, EmailCompany, PhoneCompany, ProjectCompany, Like, Message, InteractionInformationCompany


admin.site.register(Company)
admin.site.register(PhoneCompany)
admin.site.register(EmailCompany)
admin.site.register(ProjectCompany)
admin.site.register(Like)
admin.site.register(Message)
admin.site.register(InteractionInformationCompany)
