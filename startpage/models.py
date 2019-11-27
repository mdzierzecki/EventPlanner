from django.db import models
from django.contrib.auth.models import User


class eUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    from_where = models.TextField()