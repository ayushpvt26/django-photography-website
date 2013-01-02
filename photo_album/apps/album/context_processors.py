from apps.album.models import Album, Event


def nav_lists(context):
    return { 'event_nav_lsit' : Event.objects.all()[:10], 'album_nav_lsit' : Album.objects.all()[:10] }
