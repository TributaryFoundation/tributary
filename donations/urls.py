from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start$', views.start, name='start'),
    url(r'^info$', views.info, name='info'),
    url(r'^received$', views.received, name='received'),
    url(r'^confirmed$', views.confirmed, name='confirmed'),
]
