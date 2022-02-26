from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile = models.TextField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=40, null=True, blank=True)

    name = models.CharField(max_length=40, null=False, blank=False)
    phone = models.CharField(max_length=40, null=True, blank=True)

    is_valid = models.BooleanField(default=False)

    marketing = models.BooleanField(default=True)
