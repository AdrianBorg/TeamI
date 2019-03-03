from django.conf.urls import url
from trimit import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    # url(r'popup/$', views.popupTest, name='popup'),
    url(r'^register/(?P<account_type>(user|hairdresser))/$', views.register, name='register'),
    url(r'^register/user$', views.register, name='user_register'),
    url(r'^register/hairdresser$', views.register, name='hairdresser_register'),
    url(r'ajax/user_login/$', views.ajax_user_login, name='ajax_user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]