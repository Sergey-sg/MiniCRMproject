from django.urls import path, include

from .views import views, views_likes, view_companies, user_views

urlpatterns = [
    path('', view_companies.CompanyListView.as_view(), name='home'),
    path('company/', include([
        path('create/', view_companies.CompanyCreateView.as_view(), name='company-create'),
        path('<int:pk>/', include([
            path('detail/', view_companies.CompanyDetailView.as_view(), name='company_detail'),
            path('update/', view_companies.CompanyUpdateView.as_view(), name='company-update'),
            path('projects/', views.ProjectCompanyListView.as_view(), name='company-projects'),
            path('messages/', view_companies.MessageCompanyListView.as_view(), name='company-messages'),
        ])),
    ])),
    path('project/', include([
        path('<int:pk>/', include([
            path('detail/', views.ProjectWithMessageListView.as_view(), name='project_detail'),
            path('update/', views.ProjectCompanyUpdateView.as_view(), name='project-update'),
            path('new-message/', views.MessageCreateView.as_view(), name='message_create'),
        ])),
        path('create/', views.ProjectCompanyCreate.as_view(), name='project-create'),
        path('message/<int:pk>/', include([
            path('detail/', views.MessageDetailView.as_view(), name='message_detail'),
            path('update/', views.MessageUpdateView.as_view(), name='message-update'),
            ])),
    ])),
    path('likes/', include([
            path('add/', views_likes.AddLikeView.as_view(), name='add'),
            path('add-dislike/', views_likes.AddDisLikeView.as_view(), name='add_dislike'),
            path('remove/', views_likes.RemoveLikeView.as_view(), name='remove'),
            path('remove-dislike/', views_likes.RemoveDisLikeView.as_view(), name='remove_dislike'),
            ],)),
    path('accounts/', include([
        path('login/', user_views.CustomLoginView.as_view(), name='login'),
        path('create/', user_views.UserCreateView.as_view(), name='create_user'),
        path('profile/', views.PersonalArea.as_view(), name='personal-area'),
        path('change/', user_views.UserChangeView.as_view(), name='user-change'),
        path('password/', user_views.MyPasswordChangeView.as_view(), name='password-change'),
        ]),)
]
