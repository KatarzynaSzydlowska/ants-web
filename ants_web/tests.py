# -*- coding: utf-8 -*-
#from unittest import TestCase
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.sessions.middleware import SessionMiddleware

from models import *
from views import *


class CourseManagerTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create('PITE')
        self.manager = Course.objects

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

        self.termLab = Term(
            kind=2, starts_at='11:30', ends_at='13:00', location=self.location, course=self.course, day_of_week=1
        )
        self.termLab.save()

        self.term_class = Term(
            kind=3, starts_at='11:30', ends_at='13:00', location=self.location, course=self.course, day_of_week=1
        )
        self.term_class.save()
        self.term_class.instructors.add(self.instructor1)

        self.term_class_2 = Term(
            kind=3, starts_at='11:30', ends_at='13:00', location=self.location, course=self.course, day_of_week=1
        )
        self.term_class_2.save()
        self.term_class_2.instructors.add(self.instructor1)

        self.term_class_3 = Term(
            kind=3, starts_at='11:30', ends_at='13:00', location=self.location, course=self.course, day_of_week=1
        )
        self.term_class_3.save()
        self.term_class_3.instructors.add(self.instructor1)

        self.term_lecture = Term(
            kind=1, starts_at='11:30', ends_at='13:00', location=self.location, course=self.course, day_of_week=1
        )
        self.term_lecture.save()
        self.term_lecture.instructors.add(self.instructor1)

        self.term_class2 = Term(
            kind=3, starts_at='11:30', ends_at='13:00', location=self.location, course=self.course2, day_of_week=1
        )
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


class TermTestCase(TestCase):
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


class StudentTestCase(TestCase):
    def setUp(self):
        self.student = Student(index=123, name="Pawel", surname="Semon", group_id="3", password="testpassword")

    def test__str__(self):
        self.assertEqual(self.student.__str__(), "Pawel Semon")

    def test_get_hashed_password(self):
        self.assertEqual(
            make_password(self.student.password, None, hasher='unsalted_md5'),
            self.student.get_hashed_password(self.student.password)
        )


class StudentManagerTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            index=123, name="Pawel", surname="Semon", group="3", password="testpassword"
        )

    def test_create(self):
        self.assertEqual(self.student.index, self.student.index)
        self.assertEqual(self.student.name, self.student.name)
        self.assertEqual(self.student.surname, self.student.surname)
        self.assertEqual(self.student.group_id, self.student.group_id)
        self.assertEqual(self.student.password, Student.get_hashed_password("testpassword"))


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.student = Student(
            index=123, name="Pawel", surname="Semon", group_id="3", password="testpassword"
        )
        self.student.is_activated = True
        self.student.save()

    def test_index_guest(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logowanie')

    def test_index_user(self):
        request = self.factory.get(reverse('index'))
        request.session = {'user': self.student.id}
        response = index_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zalogowany jako ' + self.student.name + ' '+self.student.surname)

    def test_index_go_to_login(self):
        request = self.factory.get(reverse('index'))
        request.session = {'user': None}
        response = index(request)
        self.assertContains(response, 'Logowanie')

    def test_index_go_to_dashboard(self):
        request = self.factory.get(reverse('index'))
        request.session = {'user': self.student.id}
        response = index_user(request)
        self.assertEqual(response.status_code, 200)

    def test_login_go_to_password_change(self):
        self.student.is_activated = False
        self.student.save()
        request = self.factory.post('/login/', {'index_number': '123', 'password': 'passwordtest'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        response = login(request)
        self.assertRedirects(response, reverse('change_password'))

    def test_negative_login(self):
        request = self.factory.post(reverse('login'), {'index_number': '123', 'password': 'test'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_positive_login(self):
        request = self.factory.post(reverse('login'), {'index_number': '123', 'password': 'passwordtest'})
        #middleware = SessionMiddleware()
        #middleware.process_request(request)
        #request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 200)

'''
    #def test_change_password(self):
    #    #request = self.factory.get('/change_password')
    #    request = self.factory.post('/change_password', {'user': '', 'password': 'passwordtest'})
    #    middleware = SessionMiddleware()
    #    middleware.process_request(request)
    #    request.session.save()
    #    response = logout(request)
    #    response = change_password(request)
    #    self.assertEqual(response.status_code, 200)

    #PASS




    #)
'''

