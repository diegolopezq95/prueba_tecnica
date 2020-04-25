from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/greetings/(?P<pk>[0-9]+)$', views.greetings_get),
    url(r'^v1/greetings', views.greetings_post),
]