from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^demo/start$', views.start, name='start'),
    url(r'^demo/info$', views.info, name='info'),
    url(r'^demo/received$', views.received, name='received'),
    url(r'^demo/confirmed$', views.confirmed, name='confirmed'),
]
