import csv

from django.core.management.base import BaseCommand

from ants_web.models import Student


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename'], 'rb') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for row in reader:
                try:
                    student = Student.objects.get(index=row[0])
                    student.name = row[1]
                    student.surname = row[2]
                    student.password = Student.get_hashed_password(row[2] + row[1])
                    student.group_id = row[3]
                except Student.DoesNotExist:
                    student = Student.objects.create(
                        index=row[0],
                        name=row[1],
                        surname=row[2],
                        password=Student.get_hashed_password(row[2] + row[1]),
                        group=row[3],
                    )

                student.save()
                self.stdout.write(self.style.SUCCESS('Student %s was created' % row[0]))