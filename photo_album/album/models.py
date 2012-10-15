import string
import urllib
from datetime import datetime

from PIL import Image, ExifTags

from django.db.models.signals import pre_save
from django.db import models

# TODO: Refactor event and album in to generic image collection class
class Event(models.Model):

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
        return ('event-detail', (), {'slug': self.slug})

    def _get_lat_long(self):
        url = 'http://maps.google.com/maps/geo?q=%s&output=csv&sensor=false' % self.location
        feed = urllib.urlopen(url)
        (status, accuracy, latitude, longitude) = string.split(feed.read(), ',')
        if int(status) == 200:
            self.latitude = latitude
            self.longitude = longitude

    def save(self, *args, **kwargs):
        self._get_lat_long()
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    @property
    def cover_image(self):
        try:
            return self.photo_set.all()[0]
        except IndexError:
            return None

    @property
    def preview_images(self):
        return self.photo_set.all()[0:5]

    class Meta:
        ordering = ('-date_created',)

class Album(models.Model):

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @models.permalink
    def get_absolute_url(self):
        return ('album-detail', (), {'slug': self.slug})

    def __unicode__(self):
        return self.title

    @property
    def cover_image(self):
        try:
            return self.photo_set.all()[0]
        except IndexEror:
            return None

    class Meta:
        ordering = ('title',)

class Photo(models.Model):

    # This is the most important bit!
    picture = models.ImageField(upload_to='album/photo/%Y/%m/')

    # Meta data
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
    
    class Meta:
        ordering = ('order',)

    def _read_exif(self):
        # Reads EXIF from the photo
        # See: http://www.exif.org/specifications.html
        exposure_programs = {
            0 : 'Not defined',
            1 : 'Manual',
            2 : 'Normal program',
            3 : 'Aperute priority',
            4 : 'Shutter priority',
            5 : 'Creative program',
            6 : 'Action program',
            7 : 'Portrait mode',
            8 : 'Landscape mode',
        }

        metering_modes = {
            0 : 'unknown',
            1 : 'Average',
            2 : 'Center Weighted Average',
            3 : 'Spot',
            4 : 'Multi Spot',
            5 : 'Pattern',
            6 : 'Partial',
            'Other' : 'reserved',
            255 : 'other',
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
            #   2012:09:29 11:44:19
            self.date_time_taken = datetime.strptime(exif_data[36867], "%Y:%m:%d %H:%M:%S") 
        except KeyError:
            pass

    @property
    def get_disqus_url(self):
        return 'http://photos.danux.co.uk%s' % self.get_absolute_url()

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        self._read_exif()
        super(Photo, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('photo-detail', (), {'slug': self.slug})

    def __unicode__(self):
        return self.title