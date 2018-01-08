from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^test/$', views.test),
    url(r'^card/(?P<card_id>\w+)/$', views.card),
    url(r'^reset/$', views.reset),
    url(r'^logout/$', views.logout),
    url(r'^data/(?P<game_data_id>\w+)/$', views.data),
]