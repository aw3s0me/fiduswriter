from django.conf.urls import url

from . import views

urlpatterns = [
    url('^hierarchy/$', views.hierarchy, name='hierarchy'),
]