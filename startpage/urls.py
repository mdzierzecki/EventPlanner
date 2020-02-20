from django.conf.urls import url
from django.urls import path

from .views import startpage, UserRegisterView, logout_view, UserLoginView, user_help_view

urlpatterns = [
    path('', startpage),
    path('register-account/',
         UserRegisterView.as_view(), name="register_account"),
    path('login/',
         UserLoginView.as_view(), name="login_view"),
    path('logout/',
         logout_view, name="logout_view"),


    path('help/', user_help_view, name="help_view"),
]