from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^course_join/(?P<course_id>[0-9]+)/$', views.course_join, name='course_join'),
    url(r'^course_leave/(?P<course_id>[0-9]+)/$', views.course_leave, name='course_leave'),
    url(r'^course_details/(?P<course_id>[0-9]+)/$', views.course_details, name='course_details'),
    url(r'^course_list/$', views.course_list, name='course_list'),
    url(r'^terms_selection/$', views.terms_selection, name='terms_selection'),
]
