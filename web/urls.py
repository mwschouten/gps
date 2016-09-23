from django.conf.urls import patterns, include, url
from web.views import index

urlpatterns = [
        url(r'^$', index, name='web'),
        ]
