from django.test.client import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from views import *
from unittest import TestCase
from ants_web.models import Course, CourseManager
from ants_web.models import StudentManager
from ants_web.models import Student
from django.contrib.auth.hashers import make_password

class CourseManagerTestCase(TestCase):
    def setUp(self):
        self.course = Course('PITE')
        self.courseManager = CourseManager()

    #FAIL
    def test_create(self):
        self.assertEqual(self.courseManager.create('PITE').name, self.course.name)


    #def test_get_or_create(self):
    #    self.assertEqual(self.courseManager.get_or_create('PITE').name, self.course.name)


class CourseTestCase(TestCase):
    def setUp(self):
        self.expected = ['foo', 'bar', 'baz']
        self.result = ['baz', 'foo', 'bar', 'bar']
        self.course = Course()

    #FAIL
    def test___init__(self):
        course = Course('Python in the enterprise')
        self.assertEqual(course.name, 'Python in the enterprise')

    def test_get_instructors(self):
        print(self.course.get_instructors())
        #self.assertItemsEqual(self.course.get_instructors(), self.result)

    #def test_validate_points(self):
    #    self.assertTrue(self.course.validate_points(10))
    #    self.assertFalse(self.course.validate_points(20))

    #def test_get_choosable_terms(self):
    #    print(self.course.get_choosable_terms())
    #    self.assertItemsEqual(self.course.get_choosable_terms(), self.result)

class StudentTestCase(TestCase):
    def setUp(self):
        self.student = Student(index = 123, name = "Pawel", surname = "Semon", group_id = "3", password = "testpassword")

    #PASS
    def test__str__(self):
        self.assertEqual(self.student.__str__(), "Pawel Semon")
    #PASS
    def test_get_hashed_password(self):
        self.assertEqual(make_password(self.student.password, None, hasher='unsalted_md5'), self.student.get_hashed_password(self.student.password))

class StudentManagerTestCase(TestCase):
    def setUp(self):
        self.student = Student(index = 123, name = "Pawel", surname = "Semon", group_id = "3", password = "testpassword")

    #PASS
    def test_create(self):
        self.assertEqual(StudentManager.create(123, "Pawel", "Semon", "3", "testpassword").index, self.student.index)
        self.assertEqual(StudentManager.create(123, "Pawel", "Semon", "3", "testpassword").name, self.student.name)
        self.assertEqual(StudentManager.create(123, "Pawel", "Semon", "3", "testpassword").surname, self.student.surname)
        self.assertEqual(StudentManager.create(123, "Pawel", "Semon", "3", "testpassword").group_id, self.student.group_id)
        self.assertEqual(StudentManager.create(123, "Pawel", "Semon", "3", "testpassword").password, Student.get_hashed_password(self.student.password))

class ViewTestCase(TestCase):
    def setUp(self):
        self.template = loader.get_template('login.html')
        self.client = Client()
        self.factory = RequestFactory()

    #PASS
    def test_negative_login(self):
        #request = self.factory.get('/login')
        request = self.factory.post('/login/', {'index_number': '123', 'password': 'test'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 200)

    #PASS
    def test_positive_login(self):
        #request = self.factory.get('/login')
        request = self.factory.post('/login/', {'index_number':'123' , 'password':'passwordtest'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 200)

    #PASS
    def test_logout(self):
        request = self.factory.get('/logout')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = logout(request)
        self.assertEqual(response.status_code, 302)

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
    def test_index_guest(self):
        request = self.factory.get('/login')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = index(request)
        self.assertEqual(response.status_code, 200)

    #def test_index_user(self):
    #    request = self.factory.get('/login')
    #    middleware = SessionMiddleware()
    #    middleware.process_request(request)
    #    request.session.save()
    #    response = index(request)
    #    self.assertEqual(response.status_code, 200)

    #def test_activated_index_user(self):
    #    request = self.factory.post('/change_password', {'user': '', 'password': 'passwordtest'})
    #    middleware = SessionMiddleware()
    #    middleware.process_request(request)
    #    request.session.save()
    #    response = login(request)
    #    response = index_user(request)
    #    self.assertEqual(response.url, 'change_password/')
