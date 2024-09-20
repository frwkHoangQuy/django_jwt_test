import os

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from User.models import User

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


def upload_to(instance, filename):
    name, ext = os.path.splitext(filename)

    return os.path.join(name, filename)


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.CharField(max_length=10000)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    user = models.ForeignKey(User, related_name='snippets', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        ordering = ['created']
