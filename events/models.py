from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


class Event(models.Model):

    # event statuses
    ACTIVE = 'Active event'
    INACTIVE = 'Stopped event'
    PAUSED = 'Paused event'

    EVENT_STATUS_CHOICES = (
        (ACTIVE, _('Active event')),
        (INACTIVE, _('Stopped event')),
        (PAUSED, _('Paused event'))
    )

    # basic informations
    title = models.CharField(max_length=128, null=True)

    # location
    city = models.CharField(max_length=64, null=True)
    street = models.CharField(max_length=64, null=True)

    # event description
    description = RichTextUploadingField(null=True)
    contact_description = RichTextUploadingField(null=True, blank=True)

    # status
    event_status = models.CharField(max_length=64, choices=EVENT_STATUS_CHOICES,
                                         default=ACTIVE, null=True)

    # date of event
    date = models.DateField()

    # social media

    facebook = models.CharField(max_length=64, null=True)
    website = models.CharField(max_length=64, null=True)

    # footer
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("When event was created")
    )

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reg_date = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("When participant jointed event")
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['reg_date']