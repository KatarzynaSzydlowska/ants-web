# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory

from antsWeb.ants_web.models import Location
from views import *


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.student1 = Student.objects.create(index=123, name="Paweł", surname="Ćwięreśniak", group_id=1,
                                              is_activated=True, password="testpassword")
        self.student1.save()

        self.student2 = Student.objects.create(index=124, name="Micz", surname="Logan", group_id=2,
                                               is_activated=True, password="testpassword")
        self.student2.save()

        self.course = Course(name='Pite')
        self.course.save()

        self.location = Location(name='D10, 206', capacity=15)
        self.location.save()

        self.term = Term(kind=2, starts_at='11:30', ends_at='13:00', location=self.location,
                         course=self.course, day_of_week=1)
        self.term.save()

        self.selection = TermSelection.objects.create_or_update(student_id=self.student1.id,
                                                                term_id=self.term.id,
                                                                points=5, comment='testowy')
        self.selection.save()

    def test_check_privileges(self):
        self.assertTrue(check_privileges(self.student1))
        self.assertFalse(check_privileges(self.student2))

    def test_access_denied(self):
        session = self.client.session
        session['user'] = self.student2.id
        session.save()

        response = self.client.get(reverse('admin_term_delete', kwargs={'term_id': self.term.id}))
        self.assertNotContains(response, u'Usunięto termin.')

    def test_admin_students(self):
        session = self.client.session
        session['user'] = self.student1.id
        session.save()
        response = self.client.get(reverse('admin_students'))
        self.assertContains(response, self.student1.name)
        self.assertContains(response, self.student2.name)

    def test_admin_student_reset(self):
        session = self.client.session
        session['user'] = self.student1.id
        session.save()
        response = self.client.get(reverse('admin_student_reset', kwargs={'student_id': self.student1.id}))
        #self.assertFalse(self.student1.is_activated)
        self.assertContains(response, u'Brak dostępu.')

    def test_admin_terms(self):
        session = self.client.session
        session['user'] = self.student1.id
        session.save()
        response = self.client.get(reverse('admin_terms'))
        self.assertContains(response, self.term.kind)
        self.assertContains(response, self.term.starts_at)
        self.assertContains(response, self.term.ends_at)
        self.assertContains(response, self.term.day_of_week)

    def test_course_delete(self):
        session = self.client.session
        session['user'] = self.student1.id
        session.save()

        response = self.client.get(reverse('admin_course_delete', kwargs={'course_id': self.course.id}))
        self.assertContains(response, u'Usunięto przedmiot.')

    def test_admin_term_delete(self):
        session = self.client.session
        session['user'] = self.student1.id
        session.save()

        response = self.client.get(reverse('admin_term_delete', kwargs={'term_id': self.term.id}))
        self.assertContains(response, u'Usunięto termin.')

    def test_admin_settings(self):
        session = self.client.session
        session['user'] = self.student1.id
        session.save()

        response = self.client.get(reverse('admin_settings'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_admin_unavailable_terms(self):
        session = self.client.session
        session['user'] = self.student1.id
        session.save()
        response = self.client.get(reverse('admin_unavailable_terms', kwargs={'selection_id': self.selection.id}))
        self.assertNotContains(response, self.term.terms_names)


