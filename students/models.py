# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.db import models


class StudentManager(models.Manager):
    @classmethod
    def create(cls, index, name, surname, group_id, is_activated, password):
        hashed_password = Student.get_hashed_password(password)

        return Student(index=index, name=name, surname=surname, group_id=group_id,
                       is_activated=is_activated, password=hashed_password)


class Student(models.Model):
    index = models.IntegerField()
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    group_id = models.IntegerField()
    is_activated = models.IntegerField()
    objects = StudentManager()

    @staticmethod
    def get_hashed_password(password):
        return make_password(password, None, hasher='unsalted_md5')

    def set_new_password(self, current_password, new_password, rep_password):
        hashed_old_password = Student.get_hashed_password(current_password)

        errors = []
        if not self.password == hashed_old_password:
            errors.append(u'Błędne stare hasło.')
        elif not new_password == rep_password:
            errors.append(u'Podane hasła są róźne.')
        elif len(new_password) < 6:
            errors.append(u'Podane hasło jest zbyt krótkie.')

        if len(errors):
            return errors

        self.password = Student.get_hashed_password(new_password)
        self.is_activated = True
        return []
