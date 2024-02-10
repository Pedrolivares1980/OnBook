from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("users/register/", user_views.register, name="register"),
    path("users/login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("users/profile/", user_views.profile, name="profile"),
    path('users/edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('users/edit_profile/<int:user_id>/', user_views.edit_profile, name='admin_edit_profile'),
    path("users/logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("users/password-reset/", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset"),
    path("users/password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path("users/password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path("users/password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
    path("users/", user_views.UserAdminView, name='admin_users'),
    path("users/<int:user_id>/", user_views.user_detail, name='user_detail'),
    path("users/delete_user/<int:user_id>/", user_views.delete_user, name='delete_user'),
]

