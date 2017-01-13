# -*- coding: utf-8 -*-
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.shortcuts import render
from django.template.context_processors import csrf
from django.utils.six import StringIO

from antsWeb.ants_web.models import Course, Term
from antsWeb.students.models import Student


def check_privileges(student):
    return student.group_id == 1


def access_denied(request):
    return render(request, 'admin/access_denied.html')


def admin_students(request):
    current_student = Student.objects.get(id=request.session.get('user', 0))

    if not check_privileges(current_student):
        return access_denied(request)

    students = Student.objects.all()
    context = {'current_student': current_student, 'students': students, 'active': 'students'}

    if request.method == 'POST':
        with default_storage.open('students_import.csv', 'wb+') as destination:
            for chunk in request.FILES['importFile'].chunks():
                destination.write(chunk)

        out = StringIO()
        call_command('import_students_from_csv', 'students_import.csv', stdout=out, no_color=True)
        default_storage.delete('students_import.csv')
        context.update({'messages': out.getvalue().split("\n")})

    context.update(csrf(request))
    return render(request, 'admin/students.html', context)


def admin_student_reset(request, student_id):
    current_student = Student.objects.get(id=request.session.get('user', 0))

    if not check_privileges(current_student):
        return access_denied(request)

    student = Student.objects.get(id=student_id)
    students = Student.objects.all()
    context = {'current_student': student, 'students': students}

    student.password = Student.get_hashed_password(student.surname + student.name)
    student.is_activated = False
    student.save()
    context.update({'successes': [u'Hasło zostało zresetowane']})

    return render(request, 'admin/students.html', context)


def admin_terms(request):
    current_student = Student.objects.get(id=request.session.get('user', 0))

    if not check_privileges(current_student):
        return access_denied(request)

    courses = Course.objects.all()
    context = {'current_student': current_student, 'courses': courses, 'active': 'terms'}

    if request.method == 'POST':
        with default_storage.open('students_terms.csv', 'wb+') as destination:
            for chunk in request.FILES['importFile'].chunks():
                destination.write(chunk)

        out = StringIO()
        call_command('import_terms_from_csv', 'students_terms.csv', stdout=out, no_color=True)
        default_storage.delete('students_terms.csv')
        context.update({'messages': out.getvalue().split("\n")})

    context.update(csrf(request))
    return render(request, 'admin/terms.html', context)


def admin_course_delete(request, course_id):
    current_student = Student.objects.get(id=request.session.get('user', 0))

    if not check_privileges(current_student):
        return access_denied(request)

    context = {'current_student': current_student, 'active': 'terms'}

    course = Course.objects.get(id=course_id)
    course.delete()
    context.update({'successes': [u'Usunięto przedmiot.']})
    courses = Course.objects.all()
    context.update({'courses': courses})

    return render(request, 'admin/terms.html', context)


def admin_term_delete(request, term_id):
    current_student = Student.objects.get(id=request.session.get('user', 0))

    if not check_privileges(current_student):
        return access_denied(request)

    context = {'current_student': current_student, 'active': 'terms'}

    course = Term.objects.get(id=term_id)
    course.delete()
    context.update({'successes': [u'Usunięto termin.']})
    courses = Course.objects.all()
    context.update({'courses': courses})

    return render(request, 'admin/terms.html', context)


def admin_settings(request):
    current_student = Student.objects.get(id=request.session.get('user', 0))

    if not check_privileges(current_student):
        return access_denied(request)

    context = {'current_student': current_student}
    return render(request, 'admin/settings.html', context)
