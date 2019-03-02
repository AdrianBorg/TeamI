from django.conf.urls import url
from trimit import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'popup/$', views.popupTest, name='popup'),
    url(r'user_register/$', views.user_register, name='user_register'),
    # url(r'^ajax/register_user/$', views.ajax_user_register, name='ajax_user_register'),
]