from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from album.models import Album, Event, Photo

class AlbumDetailView(DetailView):

    queryset = Album.objects.all()

    def get_object(self):
        object = super(AlbumDetailView, self).get_object()
        return object

class EventDetailView(DetailView):

    queryset = Event.objects.all()

    def get_object(self):
        object = super(EventDetailView, self).get_object()
        return object

class PhotoDetailView(DetailView):

    queryset = Photo.objects.all()

    def get_object(self):
        object = super(PhotoDetailView, self).get_object()
        return object