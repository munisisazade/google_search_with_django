from django.conf.urls import url

from django.contrib.auth import views as auth_views

from . import views
from spider.views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/$', views.Search , name='search'),
    #url(r'^news/$', views.news_single, name='single'),
]
