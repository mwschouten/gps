from django.conf.urls import url
from files import views

urlpatterns = [
    # url(r'^list/$', views.list, name='list'),
    url(r'^submit$', views.submit, name='submit'),
	]