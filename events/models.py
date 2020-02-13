from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


class Event(models.Model):

    # event statuses
    ACTIVE = 'Aktywne'
    ENDED = 'Zakończone'
    PAUSED = 'Wstrzymane'

    EVENT_STATUS_CHOICES = (
        (ACTIVE, _('Aktywne')),
        (ENDED, _('Zakończone')),
        (PAUSED, _('Wstrzymane'))
    )

    # basic informations
    title = models.CharField(max_length=128, null=True)

    # location
    city = models.CharField(max_length=64, null=True)
    street = models.CharField(max_length=64, null=True)

    # event description
    description = RichTextUploadingField(null=True)
    contact_description = RichTextUploadingField(null=True, blank=True)

    # date of event
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    # status
    event_status = models.CharField(max_length=64, choices=EVENT_STATUS_CHOICES,
                                         default=ACTIVE, null=True)

    # social media
    facebook = models.CharField(max_length=64, null=True, blank=True)
    website = models.CharField(max_length=64, null=True, blank=True)

    # stats
    participants_amount = models.PositiveIntegerField(default=0)  # amount of participants added to event
    event_views = models.PositiveIntegerField(default=0)  # counter of events views

    # additional field
    if_additional_field = models.BooleanField(default=False)
    additional_field = models.CharField(max_length=70, null=True, blank=True)

    # participants limit
    if_participants_limit = models.BooleanField(default=False)
    participants_limit = models.PositiveIntegerField(default=0, null=True, blank=True)

    # footer
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("When event was created")
    )

    def __str__(self):
        return self.title


class Participant(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    additional_field = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reg_date = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("When participant jointed event")
    )

    def save(self, force_insert=False, force_update=False):
        # if self.id is None:
        self.event.participants_amount +1
        self.event.save()

        super(Participant, self).save(force_insert, force_update)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['reg_date']