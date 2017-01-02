# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory

from models import *
from views import *


class StudentTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(index=123, name="Paweł", surname="Ćwięreśniak", group_id=3,
                                              is_activated=False, password="testpassword")

    def test_get_hashed_password(self):
        self.assertEqual(make_password(self.student.password, None, hasher='unsalted_md5'),
                         self.student.get_hashed_password(self.student.password))

    def test_change_password_wrong_old_one(self):
        result = self.student.set_new_password('testpassword0', 'testtest', 'testtest')
        self.assertIn(u'Błędne stare hasło.', result)

    def test_change_password_different(self):
        result = self.student.set_new_password('testpassword', 'testtest', 'testtest0')
        self.assertIn(u'Podane hasła są róźne.', result)

    def test_change_password_too_short(self):
        result = self.student.set_new_password('testpassword', 'test', 'test')
        self.assertIn(u'Podane hasło jest zbyt krótkie.', result)

    def test_change_password_positive(self):
        result = self.student.set_new_password('testpassword', 'testtest', 'testtest')
        self.assertEqual([], result)
        self.assertTrue(self.student.is_activated)


class StudentManagerTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(index=123, name="Paweł", surname="Ćwięreśniak", group_id=3,
                                              is_activated=False, password="testpassword")

    def test_manager_create(self):
        self.assertEqual(self.student.index, 123)
        self.assertEqual(self.student.name, "Paweł")
        self.assertEqual(self.student.surname, "Ćwięreśniak")
        self.assertEqual(self.student.group_id, 3)
        self.assertEqual(self.student.password, Student.get_hashed_password("testpassword"))


class StudentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.student = Student.objects.create(index=123, name="Paweł", surname="Ćwięreśniak", group_id=3,
                                              is_activated=True, password="testpassword")
        self.student.save()

        self.student2 = Student.objects.create(index=122, name="Jacek", surname="Ćwięreśniak", group_id=3,
                                               is_activated=False, password="testpassword")
        self.student2.save()

    def test_index_guest(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logowanie')

    def test_index_user(self):
        request = self.factory.get(reverse('index'))
        request.session = {'user': self.student.id}
        response = index_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zalogowany jako ' + self.student.name + ' ' + self.student.surname)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'index_number': 122, 'password': 'testpassword0'})
        self.assertContains(response, 'Błędny login lub hasło.')

    def test_login_success_activated(self):
        response = self.client.post(reverse('login'), {'index_number': 123, 'password': 'testpassword'})
        self.assertRedirects(response, reverse('index'))

    def test_login_success_not_activated(self):
        response = self.client.post(reverse('login'), {'index_number': 122, 'password': 'testpassword'})
        self.assertRedirects(response, reverse('change_password'))

    def test_password_change_success(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        response = self.client.post(
            reverse('save_new_password'),
            {'old_password': 'testpassword', 'new_password': 'testtest', 'repeat_password': 'testtest'}
        )

        self.assertContains(response, u'Hasło zostało zmienione.')

    def test_password_change_failure(self):
        session = self.client.session
        session['user'] = self.student.id
        session.save()

        response = self.client.post(
            reverse('save_new_password'),
            {'old_password': 'testpassword0', 'new_password': 'testtest', 'repeat_password': 'testtest'}
        )

        self.assertContains(response, u'Błędne stare hasło.')