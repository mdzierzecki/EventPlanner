from django import forms
from .models import Mailing
from events.models import Event


class MailingAddForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.filter(author__id=1), widget=forms.Select(attrs={'class': 'form-control', }))

    class Meta:
        model = Mailing
        exclude = ('author', )
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', }),
            'zipevent_template': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'author': forms.HiddenInput,
        }

    def __init__(self, user, *args, **kwargs):
        super(MailingAddForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.filter(author=user.id)



