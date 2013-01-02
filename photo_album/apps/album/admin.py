from django.contrib import admin
from django.conf import settings
from django import forms

from apps.album.models import Photo, Event, Album


class PhotoAdmin(admin.ModelAdmin):

    date_hierarchy = 'date_created'
    
    fields = ('picture', 'title', 'slug', 'description', 'event', 'albums')

    prepopulated_fields = {"slug": ("title",)}
    
    save_on_top = True
    
    list_display = ('title', 'order',)
    
    list_editable = ('order',)
    
    list_filter = ('event',)

    class Media:
        js =(
            'https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js',
            '%sjs/jquery.ui.base.js' % settings.STATIC_URL,
            '%sjs/sortable-list.js' % settings.STATIC_URL,
        )


class PhotoInline(admin.StackedInline):

    model = Photo

    fields = ('picture', 'title', 'slug', 'albums', 'order')

    prepopulated_fields = {"slug": ("title",)}


class EventAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}

    save_on_top = True

    inlines = (PhotoInline,)
    
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js',
            '%sjs/jquery.ui.base.js' % settings.STATIC_URL,
            '%sjs/menu-sort.js' % settings.STATIC_URL,
        )


class AlbumAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}
    
    save_on_top = True


admin.site.register(Photo, PhotoAdmin)

admin.site.register(Event, EventAdmin)

admin.site.register(Album, AlbumAdmin)
