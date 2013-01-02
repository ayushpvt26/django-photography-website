from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, View, ListView

from apps.album.models import Album, Event, Photo


class AlbumListView(ListView):

    model = Album


class EventListView(ListView): 

    model = Event


class AlbumDetailView(DetailView):

    queryset = Album.objects.all()


class EventDetailView(DetailView):

    queryset = Event.objects.all()


class EventSlideshowView(EventDetailView):

    template_name = "album/slideshow.html"


class AlbumSlideshowView(AlbumDetailView):

    template_name = "album/slideshow.html"


class PhotoDetailView(DetailView):
    '''
    Base photo view. Subclassed for context specific photo views.
    '''

    model = Photo

    def get_context_data(self, **kwargs):
        '''
        Add a paginator to the context. The paginator is based 
        off the query set and will paginate photos within albums
        or events if possible.
        '''
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        photo_position = 0
        
        photo_position = list(self.get_queryset()).index(self.get_object())
        try:
            previous_photo = self.get_queryset()[photo_position-1]
        except (IndexError, AssertionError):
            previous_photo = None

        try:
            next_photo = self.get_queryset()[photo_position+1]
        except (IndexError):
            next_photo = None

        additional_context = {
            'previous_photo' : previous_photo,
            'next_photo' : next_photo,
            'current_photo_number' : photo_position + 1,
            'total_photos' : self.get_queryset().count
        }
        return dict(context.items() + additional_context.items())

    def get_queryset(self):
        '''
        Sub-classes will return a subset of their own photos if a collection
        is set.
        '''
        try:
            return self.collection.photo_set.all()
        except AttributeError:
            return super(PhotoDetailView, self).get_queryset()


class AlbumPhotoDetailView(PhotoDetailView):
    '''
    Photos when viewed in the context of an album.
    '''
    
    template_name = 'album/album_photo_detail.html'

    def get(self, *args, **kwargs):
        self.collection = get_object_or_404(Album, slug=kwargs['collection_slug'])
        return super(AlbumPhotoDetailView, self).get(*args, **kwargs)


class EventPhotoDetailView(PhotoDetailView):
    '''
    Photos when viewed in the context of an event.
    '''
    
    template_name = 'album/event_photo_detail.html'

    def get(self, *args, **kwargs):
        self.collection = get_object_or_404(Event, slug=kwargs['collection_slug'])
        return super(EventPhotoDetailView, self).get(*args, **kwargs)
