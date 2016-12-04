# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from models import Student
from django.template.context_processors import csrf
from django.contrib.auth.hashers import make_password


def index_guest(request):
    context = RequestContext(request)
    template = loader.get_template('login.html')
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def index_user(request):
    context = RequestContext(request)
    context['current_student'] = Student.objects.get(id=request.session.get('user', 0))
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context))


def login(request):
    context = RequestContext(request)
    context['current_student'] = None
    username = request.POST.get('index_number', '')
    password = request.POST.get('password', '')
    hashed_password = make_password(password, None, hasher='unsalted_md5')

    try:
        user = Student.objects.get(index=username, password=hashed_password)
        request.session['user'] = user.id
        return HttpResponseRedirect('/')
    except Student.DoesNotExist:
        context['errors'] = ["Bledny login lub haslo"]
        template = loader.get_template('login.html')
        context.update(csrf(request))
        return HttpResponse(template.render(context))


def logout(request):
    request.session['user'] = None
    return HttpResponseRedirect('/')


def index(request):
    if request.session.get('user', None) is None:
        return index_guest(request)
    else:
        return index_user(request)
