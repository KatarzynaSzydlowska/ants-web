# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory

from ants_web.templatetags.ants_web_tags import has_student_joined_course
from models import *
from views import *


class CourseManagerTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create('PITE')
        self.course.save()

    def test_create(self):
        self.assertIsInstance(self.course, Course)

    def test_create_empty_name(self):
        raised = False
        try:
            Course.objects.create('')
        except ValueError:
            raised = True

        self.assertTrue(raised)

    def test_create_name(self):
        self.assertEqual(self.course.name, 'PITE')

    def test_get_or_create_get(self):
        course = Course.objects.get_or_create('PITE')
        self.assertEqual(course.id, self.course.id)

    def test_get_or_create_create(self):
        course = Course.objects.get_or_create('PITE 2')
        self.assertIsInstance(course, Course)
        self.assertNotEqual(course.id, self.course.id)


class CourseTestCase(TestCase):
    def setUp(self):
        self.course = Course(name='Pite')
        self.course.save()

        self.course2 = Course(name='VPython')
        self.course2.save()

        self.instructor1 = Instructor(name='Tomasz Abacki', email='tomasz@abacki.pl')
        self.instructor1.save()
        self.instructor2 = Instructor(name='Tomasz Babacki', email='tomasz@babacki.pl')
        self.instructor2.save()
        self.instructor3 = Instructor(name='Tomasz Cabacki', email='tomasz@cabacki.pl')
        self.instructor3.save()

        self.location = Location(name='D10, 206', capacity=15)
        self.location.save()

        self.termLab = Term(kind=2, starts_at='11:30', ends_at='13:00', location=self.location,
                            course=self.course, day_of_week=1)
        self.termLab.save()

        self.term_class = Term(kind=3, starts_at='11:30', ends_at='13:00', location=self.location,
                               course=self.course, day_of_week=1)
        self.term_class.save()
        self.term_class.instructors.add(self.instructor1)

        self.term_class_2 = Term(kind=3, starts_at='11:30', ends_at='13:00', location=self.location,
                                 course=self.course, day_of_week=1)
        self.term_class_2.save()
        self.term_class_2.instructors.add(self.instructor1)

        self.term_class_3 = Term(kind=3, starts_at='11:30', ends_at='13:00', location=self.location,
                                 course=self.course, day_of_week=1)
        self.term_class_3.save()
        self.term_class_3.instructors.add(self.instructor1)

        self.term_lecture = Term(kind=1, starts_at='11:30', ends_at='13:00', location=self.location,
                                 course=self.course, day_of_week=1)
        self.term_lecture.save()
        self.term_lecture.instructors.add(self.instructor1)

        self.term_class2 = Term(kind=3, starts_at='11:30', ends_at='13:00', location=self.location,
                                course=self.course2, day_of_week=1)
        self.term_class2.save()
        self.term_class2.instructors.add(self.instructor3)

    def test_get_instructors(self):
        self.assertIn(self.instructor1, self.course.get_instructors())
        self.assertNotIn(self.instructor2, self.course.get_instructors())

    def test_get_terms(self):
        self.assertIn(self.term_class, self.course.get_terms())
        self.assertIn(self.term_lecture, self.course.get_terms())
        self.assertNotIn(self.term_class2, self.course.get_terms())

    def test_get_choosable_terms(self):
        self.assertIn(self.term_class, self.course.get_choosable_terms())
        self.assertNotIn(self.term_class2, self.course.get_choosable_terms())

    def test_get_validate_point_positive(self):
        points = {}
        points.update({self.term_class.id: 10})
        points.update({self.term_class_2.id: 3})
        points.update({self.term_class_3.id: 1})
        self.assertTrue(self.course.validate_points(points))

    def test_get_validate_point_negative(self):
        points = {}
        points.update({self.term_class.id: 10})
        points.update({self.term_class_2.id: 5})
        points.update({self.term_class_3.id: 1})
        self.assertFalse(self.course.validate_points(points))

    def test_get_validate_point_zero(self):
        points = {}
        points.update({self.term_class.id: 0})
        points.update({self.term_class_2.id: 0})
        points.update({self.term_class_3.id: 0})
        self.assertFalse(self.course.validate_points(points))

    def test_has_joined_course_positive(self):
        student = Student.objects.create(index=123, name="Paweł", surname="Ćwięreśniak", group_id=3,
                                         is_activated=True, password="testpassword")
        student.save()

        self.course.students.add(student)
        self.course.save()

        self.assertTrue(self.course.has_joined_course(student))

    def test_has_joined_course_negative(self):
        student = Student.objects.create(index=124, name="Jacek", surname="Ćwięreśniak", group_id=3,
                                         is_activated=True, password="testpassword")
        student.save()

        self.assertFalse(self.course.has_joined_course(student))


class TermTestCase(TestCase):
    def setUp(self):
        self.course = Course(name='Pite')
        self.course.save()

        self.location = Location(name='D10, 206', capacity=15)
        self.location.save()

        self.termLab = Term(kind=2, starts_at='11:30', ends_at='13:00', location=self.location,
                            course=self.course, day_of_week=1)
        self.termLab.save()

        self.instructor1 = Instructor(name='Tomasz Abacki', email='tomasz@abacki.pl')
        self.instructor1.save()
        self.instructor2 = Instructor(name='Tomasz Babacki', email='tomasz@babacki.pl')
        self.instructor2.save()
        self.instructor3 = Instructor(name='Tomasz Cabacki', email='tomasz@cabacki.pl')
        self.instructor3.save()

        self.termLab.instructors.add(self.instructor1)
        self.termLab.instructors.add(self.instructor2)
        self.termLab.save()

    def test_get_day_of_week_name_poniedzialek(self):
        term = Term(day_of_week=1)
        self.assertEqual(u'Poniedziałek', term.get_day_of_week_name())

    def test_get_day_of_week_name_wtorek(self):
        term = Term(day_of_week=2)
        self.assertEqual(u'Wtorek', term.get_day_of_week_name())

    def test_get_day_of_week_name_sroda(self):
        term = Term(day_of_week=3)
        self.assertEqual(u'Środa', term.get_day_of_week_name())

    def test_get_day_of_week_name_czwartek(self):
        term = Term(day_of_week=4)
        self.assertEqual(u'Czwartek', term.get_day_of_week_name())

    def test_get_day_of_week_name_piatek(self):
        term = Term(day_of_week=5)
        self.assertEqual(u'Piątek', term.get_day_of_week_name())

    def test_get_instructors(self):
        instructors = self.course.get_instructors()
        self.assertIn(self.instructor1, instructors)
        self.assertIn(self.instructor2, instructors)
        self.assertNotIn(self.instructor3, instructors)
        self.assertEqual(len(instructors), 2)

    def test_get_type_name_wyklad(self):
        term = Term(kind=1)
        self.assertEqual(u'Wykład', term.get_type_name())

    def test_get_type_name_projekt(self):
        term = Term(kind=2)
        self.assertEqual(u'Ćwiczenia Projektowe', term.get_type_name())

    def test_get_type_name_labolatorium(self):
        term = Term(kind=3)
        self.assertEqual(u'Labolatorium', term.get_type_name())

    def test_get_type_name_seminarium(self):
        term = Term(kind=4)
        self.assertEqual(u'Seminarium', term.get_type_name())

    def test_get_type_name_kurs(self):
        term = Term(kind=5)
        self.assertEqual(u'Kurs', term.get_type_name())


class TermManagerTestCase(TestCase):
    def setUp(self):
        self.course = Course(name='Pite')
        self.course.save()

        self.location = Location(name="207", capacity=15)
        self.location.save()

    def test_create(self):
        term = Term.objects.create(kind=1, starts_at='11:30', ends_at='13:00', course=self.course,
                                   day_of_week=1, location=self.location)
        self.assertIsInstance(term, Term)


class InstructorManagerTestCase(TestCase):
    def test_create(self):
        instructor = Instructor.objects.create(name='Tomasz Abacki', email='tomasz@abacki.pl')
        instructor.save()
        self.assertIsInstance(instructor, Instructor)
        self.assertEqual(instructor.name, 'Tomasz Abacki')
        self.assertEqual(instructor.email, 'tomasz@abacki.pl')

    def test_create_not_exists(self):
        instructor = Instructor.objects.create(name='Jonasz Abacki', email='jonasz@abacki.pl')
        instructor.save()
        self.assertIsInstance(instructor, Instructor)

    def test_get_or_create_get(self):
        instructor = Instructor.objects.create(name='Tomasz Abacki', email='tomasz@abacki.pl')
        instructor.save()
        instructor2 = Instructor.objects.get_or_create(name='Tomasz Abacki', email='tomasz@babacki.pl')
        instructor2.save()
        self.assertEqual(instructor.id, instructor2.id)

    def test_get_or_create_create(self):
        instructor = Instructor.objects.create(name='Tomasz Cabacki', email='tomasz@cabacki.pl')
        instructor.save()
        self.assertIsInstance(instructor, Instructor)
        self.assertEqual(instructor.name, 'Tomasz Cabacki')
        self.assertEqual(instructor.email, 'tomasz@cabacki.pl')


class LocationManagerTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name='206', capacity=15)
        self.location.save()

    def test_create(self):
        self.assertIsInstance(self.location, Location)
        self.assertEqual(self.location.name, '206')
        self.assertEqual(self.location.capacity, 15)

    def test_get_or_create_get(self):
        location = Location.objects.get_or_create(name='206', capacity=15)
        self.assertEqual(self.location.id, location.id)

    def test_get_or_create_create(self):
        location = Location.objects.get_or_create(name='207', capacity=16)
        self.assertIsInstance(location, Location)
        self.assertEqual(location.name, '207')
        self.assertEqual(location.capacity, 16)


class TermSelectionTestCase(TestCase):
    def setUp(self):
        self.course = Course(name='Pite')
        self.course.save()

        self.location = Location(name='D10, 206', capacity=15)
        self.location.save()

        self.term = Term(kind=2, starts_at='11:30', ends_at='13:00', location=self.location,
                         course=self.course, day_of_week=1)
        self.term.save()

        self.student = Student.objects.create(index=123, name="Paweł", surname="Ćwięreśniak", group_id=3,
                                              is_activated=True, password="testpassword")
        self.student.save()

        self.selection = TermSelection.objects.create_or_update(student_id=self.student.id,
                                                                term_id=self.term.id,
                                                                points=5, comment='testowy')
        self.selection.save()

    def test_create_or_update_create(self):
        self.assertIsInstance(self.selection, TermSelection)
        self.assertEqual(self.selection.student_id, self.student.id)
        self.assertEqual(self.selection.term_id, self.term.id)
        self.assertEqual(self.selection.points, 5)
        self.assertEqual(self.selection.comment, 'testowy')

    def test_create_or_update_update(self):
        selection = TermSelection.objects.create_or_update(student_id=self.student.id,
                                                           term_id=self.term.id,
                                                           points=6, comment='nie testowy')

        self.assertIsInstance(self.selection, TermSelection)
        self.assertEqual(self.selection.id, selection.id)
        self.assertEqual(selection.points, 6)
        self.assertEqual(selection.comment, 'nie testowy')


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.student = Student.objects.create(index=123, name="Paweł", surname="Ćwięreśniak", group_id=3,
                                              is_activated=True, password="testpassword")
        self.student.save()

        self.course = Course(name='PITE')
        self.course.save()
        self.course.students.add(self.student)
        self.course.save()

        self.location = Location(name='D10, 206', capacity=15)
        self.location.save()

        self.term = Term(kind=3, starts_at='11:30', ends_at='13:00', location=self.location,
                         course=self.course, day_of_week=1)
        self.term.save()

        self.term2 = Term(kind=3, starts_at='11:30', ends_at='13:00', location=self.location,
                          course=self.course, day_of_week=2)
        self.term2.save()

    def test_terms_selection(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        data = {}
        data.update({'selection[%s][points]' % self.term.id: 10})
        data.update({'selection[%s][comment]' % self.term.id: ''})
        data.update({'selection[%s][points]' % self.term2.id: 3})
        data.update({'selection[%s][comment]' % self.term2.id: 'nie dam rady'})
        response = self.client.post(reverse('terms_selection'), data)
        self.assertContains(response, 'Twój wybór został zapisany.')
        self.assertEqual(response.context[-1]['points'], {1: 10, 2: 3})
        self.assertEqual(response.context[-1]['comments'], {1: '', 2: 'nie dam rady'})

    def test_terms_selection_failure_sum(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        data = {}
        data.update({'selection[%s][points]' % self.term.id: 10})
        data.update({'selection[%s][comment]' % self.term.id: ''})
        data.update({'selection[%s][points]' % self.term2.id: 6})
        data.update({'selection[%s][comment]' % self.term2.id: 'nie dam rady'})
        response = self.client.post(reverse('terms_selection'), data)

        error = u'Dla każdego przedmiotu możesz przydzielić od 1 do 15 punktów (' + self.term.course.name + u')'
        self.assertContains(response, error)

    def test_terms_selection_failure_single(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        data = {}
        data.update({'selection[%s][points]' % self.term.id: 10})
        data.update({'selection[%s][comment]' % self.term.id: ''})
        data.update({'selection[%s][points]' % self.term2.id: 16})
        data.update({'selection[%s][comment]' % self.term2.id: 'nie dam rady'})
        response = self.client.post(reverse('terms_selection'), data)

        self.assertContains(response, u'Dla każdego terminy możesz przymisać od 1 do 10 punktów.')

    def test_terms_selection_failure_term_not_existing(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        data = {}
        data.update({'selection[%s][points]' % self.term.id: 10})
        data.update({'selection[%s][comment]' % self.term.id: ''})
        data.update({'selection[%s][points]' % 151: 6})
        data.update({'selection[%s][comment]' % 151: 'nie dam rady'})
        response = self.client.post(reverse('terms_selection'), data)
        self.assertContains(response, u'Wybrany termin nie istnieje.')

    def test_terms_selection_view(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        selection = TermSelection.objects.create_or_update(student_id=self.student.id, term_id=self.term.id,
                                                           points=10, comment='testowy')
        selection.save()

        response = self.client.get(reverse('terms_selection'))
        self.assertContains(response, self.course.name)
        self.assertContains(response, self.term.get_day_of_week_name())
        self.assertContains(response, self.term2.get_day_of_week_name())
        self.assertContains(response, selection.comment)
        self.assertEqual(response.context[-1]['points'], {selection.id: 10})
        self.assertEqual(response.context[-1]['comments'], {selection.id: 'testowy'})

    def test_course_list(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        courses = Course.objects.all()
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.context[-1]['current_student'], self.student)
        for course in courses:
            self.assertContains(response, course.name)


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(index=123, name='Tomasz', surname='Abacki', group_id=3,
                                              is_activated=True, password='testpass')
        self.student.save()

        self.student2 = Student.objects.create(index=124, name='Jacek', surname='Abacki', group_id=3,
                                               is_activated=True, password='testpass')
        self.student2.save()

        self.course = Course.objects.create('PITE')
        self.course.save()
        self.course.students.add(self.student)
        self.course.save()

    def test_has_student_joined_course(self):
        self.assertTrue(has_student_joined_course(self.student, self.course))
        self.assertFalse(has_student_joined_course(self.student2, self.course))
