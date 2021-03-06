# -*- coding: utf-8 -*-
import re

from django.shortcuts import render
from django.template.context_processors import csrf

from antsWeb.ants_admin.models import ConfigEntry
from models import Student, Course, Term, TermSelection


def terms_selection_results(request):
    student = Student.objects.get(id=request.session.get('user'))
    terms = TermSelection.objects.all().filter(student=student, selected=1)
    context = {'current_student': student, 'terms': terms}
    return render(request, 'course/terms_selection_results.html', context)


def terms_selection(request):
    context = {}
    student = Student.objects.get(id=request.session.get('user'))
    courses = Course.get_student_courses(student)

    if request.method == 'POST' and ConfigEntry.objects.get(name="selectionEnable").value == '1':
        points = {}
        comments = {}

        post_dictionary = request.POST.dict()

        for key in post_dictionary:
            result = re.search('selection\[([0-9]+)\]\[([a-z]+)\]', key)
            if result:
                if result.group(2) == 'points':
                    value = request.POST.get(key, 0)
                    points_value = int(value) if value else 0
                    points[int(result.group(1))] = points_value
                elif result.group(2) == 'comment':
                    comments[int(result.group(1))] = request.POST.get(key)

        for term_id in points:
            try:
                Term.objects.get(id=term_id)
                if points[term_id] > 10:
                    context['errors'] = [u'Dla każdego terminu możesz przymisać od 0 do 10 punktów.']
            except Term.DoesNotExist:
                context['errors'] = [u'Wybrany termin nie istnieje.']

        if 'errors' not in context:
            for course in courses:
                if not course.validate_points(points):
                    context['errors'] = [
                        u'Dla każdego przedmiotu możesz przydzielić od 1 do 15 punktów (' + course.name + u')']

        if 'errors' not in context:
            for term_id, point in points.items():
                selection = TermSelection.objects.create_or_update(
                    student_id=student.id,
                    term_id=int(term_id),
                    points=int(points[term_id]),
                    comment=comments.get(term_id, ' ')
                )
                selection.save()
                context['successes'] = ['Twój wybór został zapisany.']
    else:
        selections = TermSelection.objects.all().filter(student=student)
        points = {}
        comments = {}

        for selection in selections:
            points[selection.term.id] = selection.points
            comments[selection.term_id] = selection.comment

    context['current_student'] = student
    context['courses'] = enumerate(courses)
    context['points'] = points
    context['comments'] = comments
    context.update(csrf(request))
    return render(request, 'course/terms_selection.html', context)


def course_list(request):
    student = Student.objects.get(id=request.session.get('user'))
    context = {
        'current_student': student,
        'courses': enumerate(Course.objects.all())
    }
    return render(request, 'course/list.html', context)


def course_details(request, course_id):
    student = Student.objects.get(id=request.session.get('user'))
    context = {
        'current_student': student,
        'course': Course.objects.get(id=course_id)
    }
    return render(request, 'course/details.html', context)


def course_leave(request, course_id):
    student = Student.objects.get(id=request.session.get('user'))

    context = {
        'courses': enumerate(Course.objects.all()),
        'current_student': student
    }

    if course_id is not 0:
        course = Course.objects.get(id=course_id)
        course.students.remove(student)
        course.save()

        context['successes'] = [u'Przedmiot został usunięty z Twojej listy.']

    return render(request, 'course/list.html', context)


def course_join(request, course_id):
    student = Student.objects.get(id=request.session.get('user'))
    context = {'current_student': student}

    if course_id is not 0:
        course = Course.objects.get(id=course_id)
        course.students.add(student)
        course.save()
        context['successes'] = [u'Przedmiot został dodany do Twojej listy.']

    courses = Course.objects.all()
    context.update({'courses': enumerate(courses)})
    return render(request, 'course/list.html', context)


def terms_selection_group_results(request, term_id):
    student = Student.objects.get(id=request.session.get('user'))
    terms = TermSelection.objects.all().filter(term_id=term_id, selected=1)
    context = {'current_student': student, 'terms': terms}

    return render(request, 'course/group_results.html', context)
