# -*- coding: utf-8 -*-
# encoding=utf8
import csv
import sys

from django.core.management.base import BaseCommand

from ants_web.models import Term, Course, Instructor, Location

reload(sys)
sys.setdefaultencoding("utf-8")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename'], 'rb') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for row in reader:
                instructors_names = row[11].split("\n")
                instructors_emails = row[12].split("\n")

                instructors = []
                for i, instructor_name in enumerate(instructors_names):
                    if len(instructor_name):
                        instructor = Instructor.objects.get_or_create(
                            name=instructor_name,
                            email=instructors_emails[i]
                        )
                        instructor.save()
                        instructors.append(instructor)

                location = Location.objects.get_or_create(name=row[9], capacity=row[10])
                location.save()

                course = Course.objects.get_or_create(name=row[3])
                course.save()

                term = Term.objects.create(
                    kind=Term.terms_types[row[2].decode('utf-8')],
                    course=course,
                    location=location,
                    starts_at=row[7],
                    ends_at=row[8],
                    day_of_week=Term.days_of_week[row[4]]
                )

                term.save()

                for instructor in instructors:
                    term.instructors.add(instructor)

                term.save()
