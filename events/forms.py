from .models import Event, Participant
from django import forms
from ckeditor.fields import CKEditorWidget

class EventAddForm(forms.ModelForm):
    class Meta:
        model = Event
        description = forms.CharField(widget=CKEditorWidget)
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput,
        }


class ParticipantAddForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('event', )



