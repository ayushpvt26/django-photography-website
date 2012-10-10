from django.conf.urls import patterns, url

from album.views import AlbumDetailView, EventDetailView, photo_detail_view

urlpatterns = patterns('',
    url(r'^albums/(?P<slug>[\w\-]+)/$', AlbumDetailView.as_view(), name='album-detail'),
    url(r'^events/(?P<slug>[\w\-]+)/$', EventDetailView.as_view(), name='event-detail'),
    url(r'^photos/(?P<slug>[\w\-]+)/$', photo_detail_view, name='photo-detail'),
)