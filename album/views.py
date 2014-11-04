# -*- coding: utf-8 -*-
"""
Views for browsing photos. Photos can be views as albums, lists or slide shows.
"""
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from album.models import Album, Event, Photo


class AlbumListView(ListView):
    """
    Basic view that lists albums
    """
    model = Album


class EventListView(ListView): 
    """
    Basic view that lists events
    """
    model = Event


class AlbumDetailView(DetailView):
    """
    Basic view for an album
    """
    queryset = Album.objects.all()


class EventDetailView(DetailView):
    """
    Basic view for an event
    """
    queryset = Event.objects.all()


class EventSlideshowView(EventDetailView):
    """
    Displays an event as a slide show. It's the same view, just a new template.
    """
    template_name = "album/slideshow.html"


class AlbumSlideshowView(AlbumDetailView):
    """
    Displays an album as slideshow. It's the same view, just a new template.
    """
    template_name = "album/slideshow.html"


class PhotoDetailView(DetailView):
    """
    Base photo view. Sub-classed for context specific photo views.
    """
    model = Photo

    def __init__(self):
        super(PhotoDetailView, self).__init__()
        self.collection = None

    def get_context_data(self, **kwargs):
        """
        Add a paginator to the context. The paginator is based 
        off the query set and will paginate photos within albums
        or events if possible.

        :type kwargs: {}
        """
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        photo_position = list(self.get_queryset()).index(self.get_object())

        # Work out next and previous photos
        try:
            previous_photo = self.get_queryset()[photo_position-1]
        except (IndexError, AssertionError):
            previous_photo = None

        try:
            next_photo = self.get_queryset()[photo_position+1]
        except IndexError:
            next_photo = None

        additional_context = {
            'previous_photo': previous_photo,
            'next_photo': next_photo,
            'current_photo_number': photo_position + 1,
            'total_photos': self.get_queryset().count
        }
        return dict(context.items() + additional_context.items())

    def get_queryset(self):
        """
        Sub-classes will return a subset of their own photos if a collection
        is set.
        """
        try:
            return self.collection.photo_set.all()
        except AttributeError:
            return super(PhotoDetailView, self).get_queryset()


class ContextPhotoDetailView(PhotoDetailView):
    """
    Extendable class that will read the collection_slug param and load
    a matching object.
    """
    collection_class = None

    def __init__(self):
        super(ContextPhotoDetailView, self).__init__()
        self.collection = None

    def dispatch(self, request, *args, **kwargs):
        """
        Allows a photo to be viewed within the context of a collection
        :type request: HttpRequest
        :type args: []
        :type kwargs: {}
        :rtype: HttpResponse
        """
        self.collection = get_object_or_404(self.collection_class, slug=kwargs['collection_slug'])
        return super(ContextPhotoDetailView, self).dispatch(request, *args, **kwargs)


class AlbumPhotoDetailView(ContextPhotoDetailView):
    """
    Photos when viewed in the context of an album.
    """
    template_name = 'album/album_photo_detail.html'
    collection_class = Album


class EventPhotoDetailView(ContextPhotoDetailView):
    """
    Photos when viewed in the context of an event.
    """
    template_name = 'album/event_photo_detail.html'
    collection_class = Event
