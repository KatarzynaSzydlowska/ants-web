from django.core.management.base import BaseCommand

from ants_web.models import Student


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('index', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('group', type=int)

    def handle(self, *args, **options):
        student = Student.objects.create(index=options['index'], name=options['name'], surname=options['surname'],
                                         password=options['password'], group_id=options['group'],
                                         is_activated=True)

        student.save()
        self.stdout.write(self.style.SUCCESS('Student created.'))
