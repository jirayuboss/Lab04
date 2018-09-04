from django.contrib import admin
from tweets.models import Tweet, HashTag

admin.site.register(Tweet)
admin.site.register(HashTag)


def __str__(self):
    return self.text
