from django.contrib import admin
from album.models import Photo, Event, Album


class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    fields = ('picture', 'title', 'slug', 'description', 'event', 'albums')
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Event)
admin.site.register(Album)