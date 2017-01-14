# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Config(models.Manager):
    def set(self, name, value):
        try:
            entry = self.get(name=name)
        except ConfigEntry.DoesNotExist:
            entry = ConfigEntry()
            entry.name = name

        entry.value = value
        entry.save()


class ConfigEntry(models.Model):
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=128)
    objects = Config()
