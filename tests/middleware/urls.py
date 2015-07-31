from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^empty/$', views.empty_view),
    url(r'^non_empty/$', views.non_empty_view),
]
