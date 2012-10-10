from django.conf.urls import patterns, url

from album.views import PhotoDetailView

urlpatterns = patterns('',
    url(r'^photos/(?P<pk>\d+)/$', PhotoDetailView.as_view(), name='photo-detail'),
)