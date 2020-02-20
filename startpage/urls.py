from django.conf.urls import url
from django.urls import path

from .views import startpage, UserRegisterView, logout_view, UserLoginView, user_help_view,\
    contact_view, contact_success_view, contact_error_view

urlpatterns = [
    path('', startpage),
    path('register-account/', UserRegisterView.as_view(), name="register_account"),
    path('login/', UserLoginView.as_view(), name="login_view"),
    path('logout/', logout_view, name="logout_view"),

    path('help/', user_help_view, name="help_view"),
    path('contact/', contact_view, name="contact_view"),

    path('contact_success/', contact_success_view, name="contact_success_view"),
    path('contact_error/', contact_error_view, name="contact_error_view"),

]