from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=128)

    def __init__(self, name, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)
        self.name = name


class StudentManager(models.Manager):
    @classmethod
    def create(cls, index, name, surname, group, password):
        hashed_password = make_password(password, None, hasher='unsalted_md5')

        student = Student(
            index=index,
            name=name,
            surname=surname,
            group_id=group,
            is_activated=0,
            password=hashed_password)
        return student


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.IntegerField()
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    group_id = models.IntegerField()
    is_activated = models.IntegerField()
    objects = StudentManager()

    def __str__(self):
        return self.name + ' ' + self.surname

    @staticmethod
    def get_hashed_password(password):
        return make_password(password, None, hasher='unsalted_md5');

