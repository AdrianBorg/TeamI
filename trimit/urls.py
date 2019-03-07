from django.conf.urls import url
from trimit import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    # url(r'popup/$', views.popupTest, name='popup'),
    url(r'^user_register/$', views.user_register, name='user_register'),
    url(r'^hairdresser_register/$', views.hairdresser_register, name='hairdresser_register'),
    url(r'ajax/user_login/$', views.ajax_user_login, name='ajax_user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/(?P<search>\w{0,50})/$', views.results, name='search_results'),
    url(r'^ajax_search_results/$', views.ajax_search_filter, name='ajax_search_results'),
]