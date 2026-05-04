from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'accounts'

urlpatterns = [
    # Gestion des utilisateurs (CBV existantes)
    path('UserAdd/', views.UserAddView.as_view(), name='user_add'),
    path('userList/', views.UserListView.as_view(), name='user_list'),
    path('UserDetail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('UserUpdate/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('UserDelete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # Authentification
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # Profil (temporaire)
    path('profil/', views.UserListView.as_view(), name='profil'),
    path('profil/modifier/', views.UserUpdateView.as_view(), name='modifier_profil'),
    
    # Gestion mot de passe
    path('changer-mot-de-passe/', auth_views.PasswordChangeView.as_view(template_name='accounts/changer_mdp.html'), name='changer_mdp'),
    path('changer-mot-de-passe/fait/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/changer_mdp_done.html'), name='changer_mdp_done'),
    path('reset-mot-de-passe/', auth_views.PasswordResetView.as_view(template_name='accounts/reset_mdp.html'), name='reset_mdp'),
    path('reset-mot-de-passe/fait/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_mdp_done.html'), name='reset_mdp_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_mdp_confirm.html'), name='reset_mdp_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_mdp_complete.html'), name='reset_mdp_complete'),
]