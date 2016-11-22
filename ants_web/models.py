from __future__ import unicode_literals

from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=128)

    def __init__(self, name, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)
        self.name = name
