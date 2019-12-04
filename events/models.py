from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):

    # basic informations
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64, null=True)
    # event description
    description = models.CharField(max_length=9000, null=True)
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
    surname = models.CharField(max_length=30)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reg_date = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("When event was created")
    )

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        ordering = ['reg_date']