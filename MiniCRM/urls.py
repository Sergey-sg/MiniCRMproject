from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='home'),
    url(r'^company-detail/(?P<pk>\d+)$', views.CompanyDetailView.as_view(), name='company_detail'),
    url(r'^company/create/$', views.CompanyCreateView.as_view(), name='company-create'),
    url(r'^company/(?P<pk>\d+)/update/$', views.CompanyUpdateView.as_view(), name='company-update'),
    # url(r'^company/create/$', views.company_create, name='company-create'),
    url(r'^company/(?P<pk>\d+)/projects/$', views.ProjectCompanyListView.as_view(), name='company-projects'),
    url(r'^project-detail/(?P<pk>\d+)$', views.ProjectCompanyDetailView.as_view(), name='project_detail'),
    url(r'^project/create/$', views.ProjectCompanyCreate.as_view(), name='project-create'),
    url(r'^project/(?P<pk>\d+)/update/$', views.ProjectCompanyUpdateView.as_view(), name='project-update'),
    path('likes/', include([
        path('add/', views.AddLikeView.as_view(), name='add'),
        path('remove/', views.RemoveLikeView.as_view(), name='remove'),
        ],), name='likes'),
    url(r'^project/(?P<pk>\d+)/new-message/$', views.MessageCreateView.as_view(), name='message_create'),
    path('likes/', include([
        path('add/message-like/', views.AddMessageLikeView.as_view(), name='add-message-like'),
        path('remove/message-like/', views.RemoveMessageLikeView.as_view(), name='remove-message-like'),
        ],), name='likes'),
    url(r'^message-detail/(?P<pk>\d+)/$', views.MessageDetailView.as_view(), name='message_detail'),
    url(r'^message/(?P<pk>\d+)/update/$', views.MessageUpdateView.as_view(), name='message-update'),
    url(r'^company/(?P<pk>\d+)/messages/$', views.MessageCompanyListView.as_view(), name='company-messages'),
    url(r'^project/(?P<pk>\d+)/messages/$', views.MessageProjectListView.as_view(), name='project_messages'),
    url(r'^project/(?P<pk>\d+)/search-message/', views.message_search, name="search_message"),
    # url(r'^project-detail/(?P<pk>\d+)$', views.message_search, name='message_search'),
]
