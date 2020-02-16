import time

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mailing
from .forms import MailingAddForm
from events.models import Event, Participant
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.http import JsonResponse
import datetime


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

    participants = Participant.objects.all().filter(event=mailing.event).order_by('reg_date')

    text_content = '{}'.format(mailing.text)
    html_message = loader.render_to_string(
        'email_mailing/email_mailing.html',
        {
            'user_name': "Dupa",
            'event_title': "fas",
            'event_id': 2,
            'email_text': mailing.text,

        }
    )

    data = {
        'done': True,
    }

    for participant in participants:
        try:
            email = EmailMultiAlternatives(mailing.subject, text_content, 'Organizator <leszek@kaminski>',
                                           to=['{}'.format(participant.email)])
            email.attach_alternative(html_message, "text/html")
            email.send()
            data = {
                'done': True,
            }
            mailing.emails_sent += 1
            mailing.save()
        except:
            mailing.status = mailing.ERROR
            mailing.save()
            data = {
                'done': False,
            }
            return JsonResponse(data)
        time.sleep(4)
    mailing.status = mailing.SENT
    mailing.send_date = datetime.datetime.now()
    mailing.save()
    return JsonResponse(data)


def check_emails_sent(request):
    mailing_id = request.GET.get('mailing_id', None)
    mailing = Mailing.objects.get(pk=mailing_id)
    done = False
    if mailing.status == mailing.ERROR:
        done = True
    if mailing.participants_amount() == mailing.emails_sent:
        done = True
    data = {
        'emails_sent': mailing.emails_sent,
        'status': done
    }
    return JsonResponse(data)


class MailingDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'mailing_delete.html'
    success_message = 'Mailing został usunięty'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Mailing, id=id)

    def get_success_url(self):
        return reverse('mailing_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MailingDeleteView, self).delete(request, *args, **kwargs)