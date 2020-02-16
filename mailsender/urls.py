from django.conf.urls import url
from django.urls import path


from .views import MailingListView, EventMailingCreator, send_email, check_emails_sent, MailingDeleteView

urlpatterns = [
    # mailing
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', EventMailingCreator.as_view(), name='mailing_creator'),

    path('mailing/<int:id>/delete', MailingDeleteView.as_view(), name="mailing_delete_view"),

    url(r'^ajax/send_email/$', send_email, name='send_email'),
    url(r'^ajax/check_emails_sent/$', check_emails_sent, name='check_emails_sent'),

]