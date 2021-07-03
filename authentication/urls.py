from django.contrib import admin
from django.urls import path
from .views import RegistrationView,UserNameValidationView, EmailValidationView, VerificationView, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='Register'),
    path('username-validate', csrf_exempt(UserNameValidationView.as_view()), name='username-validate'),
    path('email-validate', csrf_exempt(EmailValidationView.as_view()), name='email-validate'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name='activate'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]