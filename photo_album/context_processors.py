# -*- coding: utf-8 -*-
"""
Provides global, no-app specific values to the templates.
"""
from django.conf import settings


def site_settings(request):
    """
    Exposes site settings to the templates.
    :type request: HttpRequest
    :return: {}
    """
    del request
    return {'MAP_API_KEY': settings.MAP_API_KEY}
