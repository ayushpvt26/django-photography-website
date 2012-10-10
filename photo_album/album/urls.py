from django.conf.urls import patterns, url

from album.views import AlbumDetailView, EventDetailView, PhotoDetailView

urlpatterns = patterns('',
    url(r'^albums/(?P<slug>[\w\-]+)/$', AlbumDetailView.as_view(), name='album-detail'),
    url(r'^events/(?P<slug>[\w\-]+)/$', EventDetailView.as_view(), name='event-detail'),
    url(r'^photos/(?P<slug>[\w\-]+)/$', PhotoDetailView.as_view(), name='photo-detail'),
)