from django.conf.urls import url
from django.urls import path


from .views import MailingListView, EventMailingCreator, send_email

urlpatterns = [
    # mailing
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', EventMailingCreator.as_view(), name='mailing_creator'),

    url(r'^ajax/send_email/$', send_email, name='send_email'),

]