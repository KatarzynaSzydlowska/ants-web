from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^course_join/(?P<course_id>[0-9]+)/$', views.course_join, name='course_join'),
    url(r'^course_leave/(?P<course_id>[0-9]+)/$', views.course_leave, name='course_leave'),
    url(r'^course_details/(?P<course_id>[0-9]+)/$', views.course_details, name='course_details'),
    url(r'^course_list/$', views.course_list, name='course_list'),
    url(r'^terms_selection/$', views.terms_selection, name='terms_selection'),
    url(r'^save_password/$', views.save_password, name='save_new_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^$', views.index, name='index'),
]
