import string, urllib
from datetime import datetime

from PIL import Image, ExifTags

from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models.signals import post_save
from django.db import models


class Event(models.Model):
    """
    An event is a way of organising photographs. Events tend to have all photos uploaded at the same time
    and are unlikely to have new photos in the future.
    """
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    latitude = models.CharField(max_length=150, blank=True, null=True)
    longitude = models.CharField(max_length=150, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @models.permalink
    def get_absolute_url(self):
        """
        Returns the absolute URL to view events.
        :return: list
        """
        return 'event-detail', (), {'slug': self.slug}

    def _get_lat_long(self):
        """
        Uses the Google maps API to work out the lat/long based on the location of the event.
        """
        url = 'http://maps.google.com/maps/geo?q={0}&output=csv&sensor=false'.format(self.location)
        feed = urllib.urlopen(url)
        (status, accuracy, latitude, longitude) = string.split(feed.read(), ',')
        if int(status) == 200:
            self.latitude = latitude
            self.longitude = longitude

    def save(self, *args, **kwargs):
        """
        Automatically works out the lat/long from the location.
        :type args: []
        :type kwargs: {}
        """
        self._get_lat_long()
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    @property
    def cover_image(self):
        """
        Returns the first photo in the set as the cover.
        :rtype: Photo | None
        """
        try:
            return self.photo_set.all()[0]
        except IndexError:
            return None

    @property
    def preview_images(self):
        """
        Returns 5 images as preview images.
        :return: QuerySet
        """
        return self.photo_set.all()[0:5]

    class Meta(object):
        """
        Specified teh default ordering
        """
        ordering = '-date_created'


class Album(models.Model):
    """
    An album is a group of photos related by a theme, e.g. nature. An album may be added to
    over time.
    """
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @models.permalink
    def get_absolute_url(self):
        """
        Returns the absolute URL to view events.
        :return: list
        """
        return 'album-detail', (), {'slug': self.slug}

    def __unicode__(self):
        return self.title

    @property
    def cover_image(self):
        """
        Returns the first photo in the set as the cover.
        :rtype: Photo | None
        """
        try:
            return self.photo_set.all()[0]
        except IndexError:
            return None

    class Meta(object):
        """
        Specifies the ordering.
        """
        ordering = 'title'


class Photo(models.Model):
    """
    A photo is the thing this site is all about! All routes lead to photos. They are an uploaded picture, belonging
    to albums and/or events. EXIF data is read from the file if present.
    """
    picture = models.ImageField(upload_to='album/photo/%Y/%m/')

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    # Internal stuff
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Parsed EXIF data - Just the bits I'm interested in, the full raw is still there
    camera = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    lens = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    shutter_speed = models.CharField(max_length=150, blank=True, null=True)
    f_number = models.CharField(max_length=150, blank=True, null=True)
    focal_length = models.CharField(max_length=150, blank=True, null=True)
    iso_speed = models.CharField(max_length=150, blank=True, null=True)
    exposure_program = models.CharField(max_length=150, blank=True, null=True)
    metering_mode = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    date_time_taken = models.DateTimeField(max_length=150, blank=True, null=True)

    # Can belong to one event and/or many albums
    event = models.ForeignKey(Event, blank=True, null=True)
    albums = models.ManyToManyField(Album, blank=True, null=True)
    
    class Meta(object):
        ordering = ('order',)

    def __unicode__(self):
        return self.title

    @property
    def get_disqus_url(self):
        """
        Returns a URL that is passed to discus to load comments
        :rtype: unicode
        """
        site = Site.objects.get(pk=settings.SITE_ID)
        return '//%s%s' % (site.domain, self.get_absolute_url())

    def save(self, *args, **kwargs):
        """
        Reads the EXIF data on save.
        :type args:
        :type kwargs:
        """
        super(Photo, self).save(*args, **kwargs)
        self._read_exif()
        super(Photo, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        """
        Permalink for photos, free of album or event context.
        :return: ()
        """
        return 'photo-detail', (), {'slug': self.slug}

    def _read_exif(self):
        # Reads EXIF from the photo
        # See: http://www.exif.org/specifications.html
        exposure_programs = {
            0: 'Not defined',
            1: 'Manual',
            2: 'Normal program',
            3: 'Aperture priority',
            4: 'Shutter priority',
            5: 'Creative program',
            6: 'Action program',
            7: 'Portrait mode',
            8: 'Landscape mode',
        }

        metering_modes = {
            0: 'unknown',
            1: 'Average',
            2: 'Center Weighted Average',
            3: 'Spot',
            4: 'Multi Spot',
            5: 'Pattern',
            6: 'Partial',
            'Other': 'reserved',
            255: 'other',
        }

        img = Image.open(self.picture.path)
        exif_data = img._getexif()

        # Determine Camera
        try:
            self.camera = exif_data[272]
        except KeyError:
            pass

        # Determine lens
        try:
            self.lens = exif_data[42036]
        except KeyError:
            pass

        # Determine shutter speed
        try:
            self.shutter_speed = '%s/%s' % exif_data[33434]
        except KeyError:
            pass

        # Determine f_number
        try:
            self.f_number = float(float(exif_data[33437][0]) / float(exif_data[33437][1]))
        except KeyError:
            pass

        # Determine focal length
        try:
            self.focal_length = int(exif_data[37386][0] / exif_data[37386][1])
        except KeyError:
            pass

        # Determine ISO speed
        try:
            self.iso_speed = exif_data[34855]
        except KeyError:
            pass
        
        # Determine exposure program
        try:
            self.exposure_program = exposure_programs[exif_data[41986]]
        except KeyError:
            pass

        # Determine meting mode
        try:
            self.metering_mode = metering_modes[exif_data[37383]]
        except KeyError:
            pass

        # Determine date time taken
        try:
            # e.g. 2012:09:29 11:44:19
            self.date_time_taken = datetime.strptime(exif_data[36867], "%Y:%m:%d %H:%M:%S") 
        except KeyError:
            pass
