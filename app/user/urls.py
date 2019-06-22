from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('auth/login/', views.LoginUserView.as_view(), name="auth-login"),
    path('auth/register/', views.RegisterUsersView.as_view(), name="auth-register"),
    path('auth/me/', views.ManageUserView.as_view(), name='me')
]
