from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User


class eUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    from_where = models.TextField()

    def save(self, force_insert=False, force_update=False):

        send_mail(
            'ZipEvent: Nowy użytkownik',
            'Zarejestrowano nowego użytkownika: {}'.format(self.user),
            'ZipEvent Team <no-reply@slickcode.pl>',
            ['mateusz@dzierzecki.com'],
            fail_silently=False,
        )
        super(eUser, self).save(force_insert, force_update)