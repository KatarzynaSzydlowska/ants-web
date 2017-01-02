from django.core.management.base import BaseCommand, CommandError

from ants_web.models import Student


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('index', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('group', type=int)

    def handle(self, *args, **options):
        student = Student.objects.create(
            index=options['index'],
            name=str(options['name']),
            surname=str(options['surname']),
            password=str(options['password']),
            group=options['group'],
        )

        try:
            student.save()
        except Student.DoesNotExist:
            raise CommandError('Student was not created')

        self.stdout.write(self.style.SUCCESS('Student created'))
