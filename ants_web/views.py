# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from models import Student
from django.template.context_processors import csrf


def index_guest(request):
    context = RequestContext(request)
    template = loader.get_template('login.html')
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def index_user(request):
    context = RequestContext(request)
    try:
        context['current_student'] = Student.objects.get(id=request.session.get('user', 0))
    except Student.DoesNotExist:
        request.session['user'] = None
        return HttpResponseRedirect('/')

    if not context['current_student'].is_activated:
        return HttpResponseRedirect('/change_password/')

    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context))


def login(request):
    context = RequestContext(request)
    context['current_student'] = None
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
        context['errors'] = ["Bledny login lub haslo"]
        template = loader.get_template('login.html')
        context.update(csrf(request))
        return HttpResponse(template.render(context))


def logout(request):
    request.session['user'] = None
    return HttpResponseRedirect('/')


def change_password(request):
    context = RequestContext(request)
    context['current_student'] = Student.objects.get(id=request.session.get('user', 0))

    template = loader.get_template('change_password.html')
    return HttpResponse(template.render(context))


def save_password(request):
    context = RequestContext(request)
    current_student = Student.objects.get(id=request.session.get('user', 0))
    context['current_student'] = current_student

    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('new_password', '')
    rep_password = request.POST.get('repeat_password', '')

    hashed_old_password = Student.get_hashed_password(old_password)

    if not current_student.password == hashed_old_password:
        context['errors'] = ["Bledne stare login"]
    elif not new_password == rep_password:
        context['errors'] = ["Podane hasla sa rozne"]
    elif len(new_password) < 6:
        context['errors'] = ["Nowe haslo jest zbyt krotkie"]

    if 'errors' not in context:
        current_student.password = Student.get_hashed_password(new_password)
        current_student.is_activated = True
        current_student.save()

        context['success'] = ["Hasło zostało zmienione"]
        template = loader.get_template('dashboard.html')
        return HttpResponse(template.render(context))
    else:
        template = loader.get_template('change_password.html')
        context.update(csrf(request))
        return HttpResponse(template.render(context))


def index(request):
    if request.session.get('user', None) is None:
        return index_guest(request)
    else:
        return index_user(request)
