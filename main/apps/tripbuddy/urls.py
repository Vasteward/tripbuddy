from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.validate_login),
    url(r'^success$', views.success),
    url(r'^create$', views.create_page),
    url(r'^create_trip$', views.create_trip),
    url(r'^trip/(?P<id>\d+)$', views.show),
]