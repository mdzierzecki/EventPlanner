import time

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mailing
from .forms import MailingAddForm
from events.models import Event
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.http import JsonResponse

from django.http import HttpResponseNotFound


class MailingListView(LoginRequiredMixin, ListView):

    template_name = 'mailing_list.html'
    model = Event
    context_object_name = 'mailing_list'

    def get_queryset(self):
        queryset = Mailing.objects.all().filter(author=self.request.user).order_by('-id')
        return queryset


class EventMailingCreator(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingAddForm
    template_name = 'mailing_create.html'

    def get_form_kwargs(self):
        kwargs = super(EventMailingCreator, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.event_id = form.instance.event.id
        obj.author = self.request.user
        obj.save()

        return HttpResponseRedirect(reverse('mailing_list'))


def send_email(request):
    mailing_id = request.GET.get('mailing_id', None)
    mailing = Mailing.objects.get(pk=mailing_id)
    mailing.status = mailing.IN_PROGRESS
    mailing.save()

    mail = "realmati@onet.pl"
    # confirmation email
    text_content = 'Dziekujemy za zapisanie na wydarzenie. Ten email jest potwierdzeniem rejestracji na wydarzenie, prosimy na niego nie odpowiadać. '
    html_message = loader.render_to_string(
        'email_mailing/email_mailing.html',
        {
            'user_name': "Dupa",
            'event_title': "fas",
            'event_id': 2,
            'email_text': mailing.text,

        }
    )

    email = EmailMultiAlternatives(mailing.subject, text_content, 'ZipEvent Team <mateusz@luksurio.pl>',
                                   to=['{}'.format(mail)])
    email.attach_alternative(html_message, "text/html")
    time.sleep(30)

    try:
        email.send()
        mailing.status = mailing.SENT
        mailing.save()
        data = {
            'done': True,
        }
        return JsonResponse(data)
    except:
        mailing.status = mailing.ERROR
        mailing.save()
        data = {
            'done': False,
        }
        return JsonResponse(data)
