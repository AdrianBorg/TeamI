from django.conf.urls import url
from trimit import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'popup/$', views.popupTest, name='popuptest'),
]