from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^save_password/$', views.save_password, name='save_new_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^$', views.index, name='index'),
]
