from django.urls import path, include

from .views import views, views_likes

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='home'),
    path('company/', include([
        path('detail/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
        path('create/', views.CompanyCreateView.as_view(), name='company-create'),
        path('<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company-update'),
        path('<int:pk>/projects/', views.ProjectCompanyListView.as_view(), name='company-projects'),
        path('<int:pk>/messages/', views.MessageCompanyListView.as_view(), name='company-messages'),
        path('likes/', include([
            path('add/', views_likes.AddLikeView.as_view(), name='add'),
            path('add-dislike/', views_likes.AddDisLikeView.as_view(), name='add_dislike'),
            path('remove/', views_likes.RemoveLikeView.as_view(), name='remove'),
            path('remove-dislike/', views_likes.RemoveDisLikeView.as_view(), name='remove_dislike'),
            ],), name='likes'),
    ])),
    path('project/', include([
        path('detail/<int:pk>/', views.ProjectWithMessageListView.as_view(), name='project_detail'),
        path('create/', views.ProjectCompanyCreate.as_view(), name='project-create'),
        path('<int:pk>/update/', views.ProjectCompanyUpdateView.as_view(), name='project-update'),
        path('<int:pk>/new-message/', views.MessageCreateView.as_view(), name='message_create'),
        path('message/', include([
            path('<int:pk>/detail/', views.MessageDetailView.as_view(), name='message_detail'),
            path('<int:pk>/update/', views.MessageUpdateView.as_view(), name='message-update'),
            path('likes/', include([
                path('add/', views_likes.AddMessageLikeView.as_view(), name='add-message-like'),
                path('add-dislike/', views_likes.AddMessageDisLikeView.as_view(), name='add_message_dislike'),
                path('remove/', views_likes.RemoveMessageLikeView.as_view(), name='remove-message-like'),
                path('remove-dislike/', views_likes.RemoveMessageDisLikeView.as_view(), name='remove_message_dislike'),
                ],), name='message_likes'),
            ])),
    ])),
    path('accounts/', include([
        path('profile/', views.PersonalArea.as_view(), name='personal-area'),
        path('change/', views.UserChangeView.as_view(), name='user-change'),
        path('password/', views.MyPasswordChangeView.as_view(), name='password-change'),
        ]),)
]
