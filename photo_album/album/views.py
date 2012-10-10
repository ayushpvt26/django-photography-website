from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from album.models import Photo

class PhotoDetailView(DetailView):

    queryset = Photo.objects.all()

    def get_object(self):
        # Call the superclass
        object = super(PhotoDetailView, self).get_object()
        # Record the last accessed date
        # object.last_accessed = timezone.now()
        # object.save()
        # Return the object
        return object