from time import timezone

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Participant
from .forms import EventAddForm, ParticipantAddForm
import csv
from django.http import HttpResponse


class EventAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = '/login'

    form_class = EventAddForm
    template_name = 'event_add.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        messages.add_message(self.request, messages.SUCCESS, 'Wydarzenie poprawnie dodane.')
        return HttpResponseRedirect(reverse('user_events_list'))


class EventDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'event_delete.html'
    success_message = 'Wydarzenie zostało usunięte'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Event, id=id)

    def get_success_url(self):
        return reverse('user_events_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EventDeleteView, self).delete(request, *args, **kwargs)


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventAddForm
    pk_url_kwarg = 'pk'
    template_name = 'event_edit.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Event, id=id)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        messages.add_message(self.request, messages.SUCCESS, 'Wydarzenie poprawnie zapisane.')
        return HttpResponseRedirect(reverse('user_events_list'))


class EventListView(LoginRequiredMixin, ListView):

    template_name = 'events_list.html'
    model = Event
    context_object_name = 'user_events_list'

    def get_queryset(self):
        queryset = Event.objects.all().filter(author=self.request.user).order_by('-id')
        return queryset


# view both for event details and participant (join) form
class EventDetailParticipantAddView(CreateView):

    model = Participant
    form_class = ParticipantAddForm
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['event'] = Event.objects.get(pk=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.event_id = self.kwargs.get('pk')
        obj.save()
        return HttpResponseRedirect(reverse('participant_successful', kwargs={'pk':self.kwargs.get('pk')}))


# Participants views

class ParticipantsListView(LoginRequiredMixin, ListView):

    template_name = 'event_members.html'
    model = Participant
    context_object_name = 'participants'

    def get_queryset(self):
        queryset = Participant.objects.all().filter(event=self.kwargs.get('id'))
        return queryset

    def get_context_data(self, **kwargs):
        participant = Event.objects.get(pk=self.kwargs['id'])
        kwargs['event'] = participant
        return super().get_context_data(**kwargs)


class ParticipantDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'participant_delete.html'
    success_message = 'Uczestnik został usunięty'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Participant, id=id)

    def get_success_url(self):
        participant = Participant.objects.get(pk=self.kwargs.get('id'))
        return reverse('event_members_view', kwargs={'id':participant.event.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ParticipantDeleteView, self).delete(request, *args, **kwargs)


# OFFER DETAIL VIEW
class ParticipantSuccessAddView(DetailView):

    model = Event
    template_name = 'participant_sucessful.html'


# view for participants export to csv
def participant_export_csv(request, event_pk):
    queryset = Participant.objects.all().filter(event=event_pk)
    ourevent = Event.objects.get(pk=event_pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails.csv"'
    writer = csv.writer(response)
    writer.writerow(['Event: {}'.format(ourevent.title)])
    writer.writerow(['Nazwa uczestnika', 'Email', 'Data rejestracji'])
    for participant in queryset:
        writer.writerow([participant.name, participant.email, participant.reg_date])

    return response