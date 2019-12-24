from time import timezone

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Participant
from .forms import EventAddForm, ParticipantAddForm


class EventAddView(LoginRequiredMixin, CreateView):
    login_url = '/login'

    form_class = EventAddForm
    template_name = 'event_add.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return redirect('/')


class EventListView(LoginRequiredMixin, ListView):

    template_name = 'events_list.html'
    model = Event
    context_object_name = 'user_events_list'

    def get_queryset(self):
        queryset = Event.objects.all().filter(author=self.request.user).order_by('-id')
        return queryset


# view both for event details and participant (join) form
class EventDetailView(CreateView):

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
        return redirect('/')


class EventDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'event_delete.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Event, id=id)

    def get_success_url(self):
        return reverse('user_events_list')

