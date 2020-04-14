from django.conf.urls import url
from django.urls import path

from .views import startpage, UserRegisterView, logout_view, UserLoginView, user_help_view,\
    contact_view, contact_success_view, contact_error_view, howitworks_startpage_view, contact_startpage_view,\
    contact_startpage_success_view, contact_startpage_error_view, faq_startpage_view

urlpatterns = [
    # landing page/startpage
    path('', startpage, name="startpage_view"),
    path('how-it-works/', howitworks_startpage_view, name="howitworks_startpage_view"),
    path('faq/', faq_startpage_view, name="faq_startpage_view"),
    path('contact/', contact_startpage_view, name="contact_startpage_view"),

    path('contact-success/', contact_startpage_success_view, name="contact_startpage_success_view"),
    path('contact-error/', contact_startpage_error_view, name="contact_startpage_error_view"),


    path('register-account/', UserRegisterView.as_view(), name="register_account"),
    path('login/', UserLoginView.as_view(), name="login_view"),
    path('logout/', logout_view, name="logout_view"),

    # inside app
    path('help/', user_help_view, name="help_view"),
    path('contact-app/', contact_view, name="contact_view"),

    path('contact-app-success/', contact_success_view, name="contact_success_view"),
    path('contact-app-error/', contact_error_view, name="contact_error_view"),

]