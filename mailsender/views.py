import time

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mailing
from .forms import MailingAddForm
from events.models import Event, Participant
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.http import JsonResponse
import datetime
from django.db.models import Q
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.auth.models import User


class MailingListView(LoginRequiredMixin, ListView):
    template_name = 'mailing_list.html'
    model = Event
    context_object_name = 'mailing_list'

    def get_queryset(self):
        queryset = Mailing.objects.all().filter(author=self.request.user).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        active_mailing_queryset = Mailing.objects.all().filter(Q(status=Mailing.IN_PROGRESS) | Q(status=Mailing.READY) | Q(status=Mailing.ERROR),
                                                               author=self.request.user)
        kwargs['can_add_event'] = True
        if len(active_mailing_queryset) >= 1:
            kwargs['can_add_event'] = False

        return super().get_context_data(**kwargs)


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
        event = Event.objects.get(pk=form.instance.event.id)
        if event.participants_amount > 250:
            messages.add_message(self.request, messages.ERROR, 'Nie możesz dodać mailingu dla wydarzenia które ma ponad 250 osób. Skontaktuj się z zespołem ZipEvent.')
            return HttpResponseRedirect(reverse('mailing_list'))

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
    html = loader.render_to_string(
        'email_mailing/email_mailing.html',
        {
            'event_title': mailing.event.title,
            'event_id': mailing.event.id,
            'email_text': mailing.text,

        }
    )

    data = {
        'done': True,
    }

    participants_list = []
    for participant in participants:
        participants_list.append(participant.email)

    user = User.objects.get(pk=request.user.id)

    participants_list.append(user.email)
    divide = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
    real_list = divide(participants_list, 90)
    print(participants_list)
    try:
        text_content = "{}".format(mailing.text)
        for part_list in real_list:
            connection = get_connection()  # uses SMTP server specified in settings.py
            connection.open()
            msg = EmailMultiAlternatives(mailing.subject, text_content, "ZipEvent Team <no-reply@slickcode.pl>", bcc=part_list,
                                         connection=connection)
            msg.attach_alternative(html, "text/html")
            msg.send()
            connection.close()  # Cleanu
            mailing.emails_sent += len(part_list)
            mailing.save()
            time.sleep(3)

        data = {
            'done': True,
        }

        mailing.emails_sent -= 1
        mailing.save()
    except:
        mailing.status = mailing.ERROR
        mailing.save()
        data = {
            'done': False,
        }
        return JsonResponse(data)
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

    def dispatch(self, request, *args, **kwargs):
        mailing = Mailing.objects.get(pk=self.kwargs.get('id'))
        if mailing.author != self.request.user:
            return HttpResponseForbidden()
        return super(MailingDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MailingDeleteView, self).delete(request, *args, **kwargs)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingAddForm
    pk_url_kwarg = 'pk'
    template_name = 'mailing_edit.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Mailing, id=id)

    def get_form_kwargs(self):
        kwargs = super(MailingUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        mailing = Mailing.objects.get(pk=self.kwargs.get('id'))
        if mailing.author != self.request.user:
            return HttpResponseForbidden()
        return super(MailingUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        event = Event.objects.get(pk=form.instance.event.id)
        if event.participants_amount > 250:
            messages.add_message(self.request, messages.ERROR,
                                 'Nie możesz dodać mailingu dla wydarzenia które ma ponad 250 osób. Skontaktuj się z zespołem ZipEvent.')
            return HttpResponseRedirect(reverse('mailing_list'))

        obj.author = self.request.user
        obj.save()
        messages.add_message(self.request, messages.SUCCESS, 'Mailing poprawnie zapisany.')
        return HttpResponseRedirect(reverse('mailing_list'))