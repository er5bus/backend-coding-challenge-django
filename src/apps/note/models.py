from django.db import models

from apps.core.behaviors import Authorable, Timestampable


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Note(Authorable, Timestampable):
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=10000)

    tags = models.ManyToManyField(Tag, related_name='notes')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
