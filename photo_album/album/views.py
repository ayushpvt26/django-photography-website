from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import render_to_response
from django.template import RequestContext

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

def photo_detail_view(request, slug):
        
    photo = get_object_or_404(Photo, slug=slug)

    album = None
    try:
        context = request.GET['context']
        if context == 'album':
            album = Album.objects.get(slug=request.GET['album'])
    except KeyError:
        pass

    return render_to_response('album/photo_detail.html', {
        'object' : photo,
        'album' : album
    }, context_instance=RequestContext(request))