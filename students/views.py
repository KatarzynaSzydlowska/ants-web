# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf

from models import Student


def index_guest(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'login.html', context)


def index_user(request):
    context = {}

    try:
        context['current_student'] = Student.objects.get(id=request.session.get('user', 0))
    except Student.DoesNotExist:
        request.session['user'] = None
        return HttpResponseRedirect('/')

    if not context['current_student'].is_activated:
        return HttpResponseRedirect('/change_password/')

    return render(request, 'dashboard.html', context)


def login(request):
    context = {'current_student': None}
    username = request.POST.get('index_number', '')
    password = request.POST.get('password', '')
    hashed_password = Student.get_hashed_password(password)

    try:
        student = Student.objects.get(index=username, password=hashed_password)
        request.session['user'] = student.id
        if student.is_activated:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/change_password/')
    except Student.DoesNotExist:

        context['errors'] = ['Błędny login lub hasło.']
        context.update(csrf(request))
        return render(request, 'login.html', context)


def logout(request):
    request.session['user'] = None
    return HttpResponseRedirect('/')


def change_password(request):
    context = {'current_student': Student.objects.get(id=request.session.get('user', 0))}
    return render(request, 'change_password.html', context)


def save_password(request):
    current_student = Student.objects.get(id=request.session.get('user', 0))
    context = {'current_student': current_student}

    old_password = str(request.POST.get('old_password', ''))
    new_password = str(request.POST.get('new_password', ''))
    rep_password = str(request.POST.get('repeat_password', ''))

    result = current_student.set_new_password(current_password=old_password, new_password=new_password,
                                              rep_password=rep_password)

    template = 'dashboard.html'
    if len(result) == 0:
        current_student.save()
        context.update({'successes': [u'Hasło zostało zmienione.']})
    else:
        context.update({'errors': result})
        context.update(csrf(request))
        template = 'change_password.html'

    return render(request, template, context)


def index(request):
    if request.session.get('user', None) is None:
        return index_guest(request)
    else:
        return index_user(request)
