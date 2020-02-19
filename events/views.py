from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from .models import Event, Participant
from .forms import EventAddForm, ParticipantAddForm, ParticipantSelfDelete
import csv
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.http import HttpResponseNotFound


class EventAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = '/login'

    form_class = EventAddForm
    template_name = 'event_add.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()

        last_user_event = Event.objects.filter(author=self.request.user).last()
        messages.add_message(self.request, messages.SUCCESS, 'Wydarzenie poprawnie dodane.')
        return redirect(reverse('event_panel_view', kwargs={'id': last_user_event.pk}))


class EventDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'event_delete.html'
    success_message = 'Wydarzenie zostało usunięte'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Event, id=id)

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs.get('id'))
        if event.author != self.request.user:
            return HttpResponseForbidden()
        return super(EventDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user_events_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EventDeleteView, self).delete(request, *args, **kwargs)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventAddForm
    pk_url_kwarg = 'pk'
    template_name = 'event_edit.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Event, id=id)

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs.get('id'))
        if event.author != self.request.user:
            return HttpResponseForbidden()
        return super(EventUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        messages.add_message(self.request, messages.SUCCESS, 'Wydarzenie poprawnie zapisane.')

        event = Event.objects.get(id=self.kwargs.get("id"))
        return redirect(reverse('event_panel_view', kwargs={'id': event.pk}))


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
        event = Event.objects.get(pk=self.kwargs['pk'])
        kwargs['event'] = event
        kwargs['participant_limit_exceeded'] = False

        if event.if_participants_limit:
            if event.participants_amount >= event.participants_limit:
                kwargs['participant_limit_exceeded'] = True

        # event views counter
        event.event_views += 1
        event.save()

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        event = Event.objects.get(pk=self.kwargs['pk'])
        if event.if_participants_limit:
            if event.participants_amount >= event.participants_limit:
                return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': self.kwargs.get('pk')}))
        obj = form.save(commit=False)
        mail = obj.email
        name = obj.name
        obj.event_id = self.kwargs.get('pk')
        obj.save()

        # participants increment counter
        event.participants_amount += 1
        event.save()

        # confirmation email
        text_content = 'Dziekujemy za zapisanie na wydarzenie. Ten email jest potwierdzeniem rejestracji na wydarzenie, prosimy na niego nie odpowiadać. '
        html_message = loader.render_to_string(
            'email_confirmation/email.html',
            {
                'user_name': name,
                'event_title': event.title,
                'event_id': event.pk,

        }
        )

        email = EmailMultiAlternatives('Potwierdzenie uczestnictwa w wydarzeniu', text_content, 'ZipEvent Team <no-reply@slickcode.pl>', to=['{}'.format(mail)])
        email.attach_alternative(html_message, "text/html")
        email.send()

        return HttpResponseRedirect(reverse('participant_successful', kwargs={'pk':self.kwargs.get('pk')}))


# Participants views

class EventPanelView(LoginRequiredMixin, ListView):

    template_name = 'event_panel.html'
    model = Participant
    context_object_name = 'participants'

    def get_queryset(self):
        queryset = Participant.objects.all().filter(event=self.kwargs.get('id'))
        return queryset

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs.get('id'))
        if event.author != self.request.user:
            return HttpResponseForbidden()
        return super(EventPanelView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        event = Event.objects.get(pk=self.kwargs['id'])
        kwargs['event'] = event

        # conversion rate shows user how many people who viewed event in real joined to the event
        if event.event_views > 0:
            conversion_rate = event.participants_amount/event.event_views
            kwargs['conversion_rate'] = round(conversion_rate, 3)

        if event.if_additional_field:
            kwargs['question_result'] = len(Participant.objects.all().filter(event=self.kwargs.get('id'), additional_field=True))

        return super().get_context_data(**kwargs)


class ParticipantDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'participant_delete.html'
    success_message = 'Uczestnik został usunięty'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Participant, id=id)

    def get_success_url(self):
        participant = Participant.objects.get(pk=self.kwargs.get('id'))

        return reverse('event_panel_view', kwargs={'id':participant.event.id})

    def dispatch(self, request, *args, **kwargs):
        participant = Participant.objects.get(pk=self.kwargs.get('id'))
        if participant.event.author != self.request.user:
            return HttpResponseForbidden()
        return super(ParticipantDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # decrement event participants counter
        participant = Participant.objects.get(pk=self.kwargs.get('id'))
        event = participant.event
        event.participants_amount -= 1
        event.save()

        messages.success(self.request, self.success_message)
        return super(ParticipantDeleteView, self).delete(request, *args, **kwargs)


def participant_self_delete_view(request):

    form = ParticipantSelfDelete(request.POST)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = ParticipantSelfDelete(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            try:
                participants = Participant.objects.filter(email=form.cleaned_data['your_email'])
            except:
                return HttpResponseRedirect(reverse('member_self_delete_error'))
            # decrement event participants counter

            if len(participants) == 0:
                return HttpResponseRedirect(reverse('member_self_delete_error'))
            for participant in participants:
                event = participant.event
                event.participants_amount -= 1
                event.save()
                participant.delete()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('member_self_delete_success'))

    context = {
        'form': form,
    }

    return render(request, 'participant_self_delete.html', context)


def participant_self_delete_success(request):
    return render(request, 'participant_self_delete_success.html')


def participant_self_delete_error(request):
    return render(request, 'participant_self_delete_error.html')


# Participant add success view
class ParticipantSuccessAddView(DetailView):

    model = Event
    template_name = 'participant_successful.html'


# view for participants export to csv
def participant_export_csv(request, event_pk):
    queryset = Participant.objects.all().filter(event=event_pk)
    our_event = Event.objects.get(pk=event_pk)
    if request.user.is_authenticated and request.user == our_event.author:
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="emails.csv"'
        writer = csv.writer(response)
        writer.writerow(['Event: {}'.format(our_event.title)])
        writer.writerow(['Nazwa uczestnika', 'Email', 'Data rejestracji'])
        for participant in queryset:
            writer.writerow([participant.name, participant.email, participant.reg_date])

        return response
    else:
        return HttpResponseNotFound("permission error")

