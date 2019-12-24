from .models import Event, Participant
from django import forms
from ckeditor.fields import CKEditorWidget


class EventAddForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', }),
            'city': forms.TextInput(attrs={'class': 'form-control', }),
            'street': forms.TextInput(attrs={'class': 'form-control', }),
            'date': forms.DateInput(attrs={'class': 'form-control', 'id': 'mdate'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'id': 'timepicker'}),
            'event_status': forms.Select(attrs={'class': 'form-control', }),
            'facebook': forms.TextInput(attrs={'class': 'form-control', }),
            'website': forms.TextInput(attrs={'class': 'form-control', }),
            'author': forms.HiddenInput,
        }


class ParticipantAddForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('event', )



