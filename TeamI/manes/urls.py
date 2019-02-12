from django.conf.urls import url
from manes import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]