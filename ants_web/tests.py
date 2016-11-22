from django.test import TestCase
from ants_web.models import Course

class CourseTestCase(TestCase):
    def test_course_can_be_created(self):
        course = Course('Python in the enterprise')
        self.assertEqual(course.name, 'Python in the enterprise')
