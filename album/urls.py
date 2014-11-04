# -*- coding: utf-8 -*-
"""
Main URL routing for the album app.
"""
from django.conf.urls import patterns, url

from album.views import AlbumDetailView, EventDetailView, EventSlideshowView
from album.views import AlbumSlideshowView, PhotoDetailView, AlbumListView, EventListView
from album.views import EventPhotoDetailView, AlbumPhotoDetailView


urlpatterns = patterns(
    '',
    url(r'^albums/$', AlbumListView.as_view(), name='album-list'),
    url(r'^events/$', EventListView.as_view(), name='event-list'),
    url(r'^albums/(?P<slug>[\w\-]+)/$', AlbumDetailView.as_view(), name='album-detail'),
    url(r'^events/(?P<slug>[\w\-]+)/$', EventDetailView.as_view(), name='event-detail'),
    url(r'^events/(?P<slug>[\w\-]+)/slideshow/$', EventSlideshowView.as_view(), name='event-slideshow'),
    url(r'^albums/(?P<slug>[\w\-]+)/slideshow/$', AlbumSlideshowView.as_view(), name='album-slideshow'),
    url(
        r'^albums/(?P<collection_slug>[\w\-]+)/(?P<slug>[\w\-]+)/$',
        AlbumPhotoDetailView.as_view(),
        name='album-photo-detail'
    ),
    url(
        r'^events/(?P<collection_slug>[\w\-]+)/(?P<slug>[\w\-]+)/$',
        EventPhotoDetailView.as_view(),
        name='event-photo-detail'
    ),
    url(
        r'^photos/(?P<slug>[\w\-]+)/$',
        PhotoDetailView.as_view(),
        name='photo-detail',
        kwargs={'collection_type': None, 'collection_slug': None}
    ),
)
