from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    ma_nv = models.IntegerField(default=-1, null=True, verbose_name="Mã nhân viên")
