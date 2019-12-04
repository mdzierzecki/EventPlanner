from .models import Event, Participant
from django import forms


class EventAddForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput
        }


class ParticipantAddForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('event', )



