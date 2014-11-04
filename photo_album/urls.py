# -*- coding: utf-8 -*-
"""
Master URL file should delegate down to apps.
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^gallery/', include('album.urls')),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name="about-page"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'photo_album.views.index'),
    url(r'^s/', include('shorty.urls', namespace='shorty')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT},)
    )
