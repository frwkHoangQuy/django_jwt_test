import os

from django.db import models


def upload_to(instance, filename):
    name, ext = os.path.splitext(filename)

    return os.path.join(name, filename)


class UploadImageTest(models.Model):
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=upload_to, blank=True, null=True)
