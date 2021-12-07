from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='home'),
    url(r'^company-detail/(?P<pk>\d+)$', views.CompanyDetailView.as_view(), name='company_detail'),
    url(r'^company/create/$', views.CompanyCreate.as_view(), name='company-create'),
    url(r'^company/(?P<pk>\d+)/update/$', views.CompanyUpdateView.as_view(), name='company-update'),
    url(r'^company/create/$', views.CompanyUpdateView.as_view(), name='company-create'),
    url(r'^company/(?P<pk>\d+)/projects/$', views.ProjectCompanyListView.as_view(), name='company-projects'),
    url(r'^project-detail/(?P<pk>\d+)$', views.ProjectCompanyDetailView.as_view(), name='project_detail'),
    url(r'^project/create/$', views.ProjectCompanyCreate.as_view(), name='project-create'),
    url(r'^project/(?P<pk>\d+)/update/$', views.ProjectCompanyUpdateView.as_view(), name='project-update'),
    path('likes/', include([
        path('add/', views.AddLikeView.as_view(), name='add'),
        path('remove/', views.RemoveLikeView.as_view(), name='remove'),
        ],), name='likes')
]
