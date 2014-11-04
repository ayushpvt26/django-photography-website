# -*- coding: utf-8 -*-
"""
Context processors to provide album data globally to the templates.
"""
from album.models import Album, Event


def nav_lists(request):
    """
    Returns albums and events for the nav lists.
    :param request:
    :return:
    """
    del request
    return {'event_nav_list': Event.objects.all()[:10], 'album_nav_list': Album.objects.all()[:10]}
