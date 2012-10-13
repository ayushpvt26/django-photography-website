from django.conf import settings

def site_settings(context):
    return { 'MAP_API_KEY': settings.MAP_API_KEY }
