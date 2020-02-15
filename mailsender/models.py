from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from events.models import Event


class Mailing(models.Model):
    READY = 'Gotowy'
    IN_PROGRESS = 'Wysyłanie'
    SENT = 'Wysłany'
    ERROR = 'Błąd'

    MAILING_STATUS_CHOICES = (
        (READY, _('Gotowy')),
        (IN_PROGRESS, _('Wysyłanie')),
        (SENT, _('Wysłany')),
        (ERROR, _('Błąd'))
    )

    subject = models.CharField(max_length=30)
    text = RichTextUploadingField()

    status = models.CharField(max_length=64, choices=MAILING_STATUS_CHOICES,
                                    default=READY, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    send_date = models.DateTimeField(
        _("Sent at"),
        auto_now_add=True,
        help_text=_("When mailing was send")
    )

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['send_date']
