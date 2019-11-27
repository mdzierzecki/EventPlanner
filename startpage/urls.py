from django.conf.urls import url
from django.urls import path

from .views import startpage, UserRegisterView

urlpatterns = [
    path('', startpage),
    path('register-account/',
         UserRegisterView.as_view(), name="register-account"),
]