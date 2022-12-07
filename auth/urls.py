from django.contrib.auth.views import LogoutView
from django.urls import path

from auth import views
from dvgm import settings

app_name = 'insecureauth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('reset_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    ]