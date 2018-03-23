from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^(?P<quote_id>\d+)/add/favorite$', views.add_favorite),
    url(r'^(?P<fav_id>\d+)/delete/favorite$', views.delete_favorite),
    url(r'^users/(?P<id>\d+)$', views.showuser),


]