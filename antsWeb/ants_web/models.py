# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from antsWeb.students.models import Student


class CourseManager(models.Manager):
    @classmethod
    def create(cls, name):
        if not len(name):
            raise ValueError(u'Nazwa przedmiotu nie może być pusta.')

        return Course(name=name)

    def get_or_create(self, name):
        try:
            return self.get(name=name)
        except Course.DoesNotExist:
            return self.create(name=name)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    students = models.ManyToManyField(Student)
    objects = CourseManager()

    def get_instructors(self):
        terms = Term.objects.all().filter(course=self)
        return Instructor.objects.all().filter(term__in=terms).distinct()

    def get_terms(self):
        return Term.objects.all().filter(course=self)

    def get_choosable_terms(self):
        return Term.objects.all().filter(course=self, kind=3).order_by('day_of_week', 'starts_at')

    def validate_points(self, points):
        terms = self.get_choosable_terms()
        points_sum = 0
        for term in terms:
            points_sum += points.get(term.id, 0)

        return 15 >= points_sum > 0

    def has_joined_course(self, student):
        return len(self.students.filter(id=student.id)) > 0

    @staticmethod
    def get_student_courses(student):
        return Course.objects.all().filter(students__course__students=student.id).distinct()


class InstructorManager(models.Manager):
    @classmethod
    def create(cls, name, email):
        return Instructor(name=name, email=email)

    def get_or_create(self, name, email):
        try:
            return self.get(name=name)
        except Instructor.DoesNotExist:
            return self.create(name=name, email=email)


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    objects = InstructorManager()


class LocationManager(models.Manager):
    @classmethod
    def create(cls, name, capacity):
        return Location(name=name, capacity=capacity)

    def get_or_create(self, name, capacity):
        try:
            return self.get(name=name)
        except Location.DoesNotExist:
            return self.create(name=name, capacity=capacity)


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    capacity = models.IntegerField(default=15)
    objects = LocationManager()


class TermManager(models.Manager):
    @classmethod
    def create(cls, kind, starts_at, ends_at, course, day_of_week, location):
        return Term(kind=kind, starts_at=starts_at, ends_at=ends_at, day_of_week=day_of_week,
                    course=course, location=location)


class Term(models.Model):
    id = models.AutoField(primary_key=True)
    kind = models.IntegerField()
    day_of_week = models.IntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructors = models.ManyToManyField(Instructor)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    objects = TermManager()

    terms_types = {
        'Wykład': 1, 'Ćwiczenia Projektowe': 2, 'Lab.': 3, 'Zajęcia Seminaryjne': 4, 'Course': 5,
        'Konwersatorium': 6}
    terms_names = {1: 'Wykład', 2: 'Ćwiczenia Projektowe', 3: 'Labolatorium', 4: 'Seminarium', 5: 'Kurs',
                   6: 'Konwersatorium'}
    days_of_week = {'M': 1, 'T': 2, 'W': 3, 'Th': 4, 'F': 5}
    days_names = {1: 'Poniedziałek', 2: 'Wtorek', 3: 'Środa', 4: 'Czwartek', 5: 'Piątek'}

    def get_instructors(self):
        return Instructor.objects.all().filter(term=self)

    def get_day_of_week_name(self):
        return self.days_names[self.day_of_week]

    def get_type_name(self):
        return self.terms_names[self.kind]


class TermSelectionManager(models.Manager):
    @classmethod
    def create_or_update(cls, student_id, term_id, points, comment):
        student = Student.objects.get(id=student_id)
        term = Term.objects.get(id=term_id)

        try:
            selection = TermSelection.objects.get(student=student, term=term)
            selection.points = points
            selection.comment = comment
        except TermSelection.DoesNotExist:
            selection = TermSelection(student=student, term=term, points=points, comment=comment)

        return selection


class TermSelection(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    points = models.IntegerField()
    comment = models.CharField(max_length=256)
    objects = TermSelectionManager()
