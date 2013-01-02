from django.conf.urls import patterns, url

from apps.album.views import AlbumDetailView, EventDetailView, EventSlideshowView
from apps.album.views import AlbumSlideshowView, PhotoDetailView, AlbumListView, EventListView


urlpatterns = patterns('',
    url(r'^albums/$', AlbumListView.as_view(), name='album-list'),
    url(r'^events/$', EventListView.as_view(), name='event-list'),
    url(r'^albums/(?P<slug>[\w\-]+)/$', AlbumDetailView.as_view(), name='album-detail'),
    url(r'^events/(?P<slug>[\w\-]+)/$', EventDetailView.as_view(), name='event-detail'),
    url(r'^events/(?P<slug>[\w\-]+)/slideshow/$', EventSlideshowView.as_view(), name='event-slideshow'),
    url(r'^albums/(?P<slug>[\w\-]+)/slideshow/$', AlbumSlideshowView.as_view(), name='album-slideshow'),
    url(r'^(?P<collection_type>(albums|events)+)/(?P<collection_slug>[\w\-]+)/(?P<slug>[\w\-]+)/$', PhotoDetailView.as_view(), name='photo-detail'),
    url(r'^photos/(?P<slug>[\w\-]+)/$', PhotoDetailView.as_view(), name='photo-detail', kwargs = {'collection_type':None, 'collection_slug':None}),
)
