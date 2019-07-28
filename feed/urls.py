from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.FeedList.as_view(), name='list'),
    url(r'^(?P<id>[0-9]+)/$', views.FeedDetails.as_view(), name='feed_retrieve'),
    url(r'^(?P<id>[0-9]+)/like/$', views.FeedLiked.as_view(), name='feed_like'),
    url(r'^(?P<id>[0-9]+)/favourite/$', views.FeedFavourite.as_view(), name='feed_favourite'),
]
