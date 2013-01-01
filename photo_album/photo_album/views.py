from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.album.models import Album, Event


def index(request):
    events = Event.objects.all()
    albums = Album.objects.all()

    return render_to_response('index.html', {
        'events':events,
        'albums':albums
    }, context_instance=RequestContext(request))
