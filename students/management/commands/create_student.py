# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from ants_web.models import Student


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('index', type=int)
        parser.add_argument('name', type=unicode)
        parser.add_argument('surname', type=unicode)
        parser.add_argument('password', type=unicode)
        parser.add_argument('group_id', type=int)

    def handle(self, *args, **options):
        student = Student.objects.create(index=options['index'],
                                         name=options['name'],
                                         surname=options['surname'],
                                         password=options['password'],
                                         group_id=options['group_id'],
                                         is_activated=True)

        student.save()
        self.stdout.write(self.style.SUCCESS('Student created.'))
