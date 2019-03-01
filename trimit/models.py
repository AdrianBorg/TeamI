from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from geopy.geocoders import GoogleV3
import datetime
from TeamI.settings import GoogleGeocodeKey
from django.conf import settings

API_KEY = GoogleGeocodeKey


class Page(models.Model):
    user = models.OneToOneField(User)
    specialities = models.CharField(max_length=30, null=True)
    flat_number = models.CharField(max_length=15, blank=True)
    street_address = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    postcode = models.CharField(max_length=30, blank=True)
    country = CountryField(blank=False)
    opening_times = models.CharField(max_length=200, null=True)
    webpage = models.URLField
    instagram = models.URLField
    picture = models.ImageField(upload_to='hairpage_images', blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    latitude = models.DecimalField(decimal_places=5, max_digits=9, blank=True, default=None)
    longitude = models.DecimalField(decimal_places=5, max_digits=9, blank=True, default=None)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        spaced_name = self.user.username.replace('_', ' ')
        self.slug = slugify(spaced_name)
        if (self.latitude is None) or (self.longitude is None):
            geolocator = GoogleV3(api_key=API_KEY)  # Nominatim(user_agent='trimit')#, country_bias='GB')
            address = self.street_address + ', ' + self.city + ', ' + self.postcode + ', ' + str(self.country)
            location = geolocator.geocode(query=address)
            if location is not None:
                if self.longitude is None:
                    self.longitude = location.longitude
                if self.latitude is None:
                    self.latitude = location.latitude
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='user_profile_images', blank=True)
    hairpicture = models.ImageField(upload_to='user_images', blank=True)

    def __str__(self):
        return self.user.username


def deleted_user():
    return get_user_model().objects.get_or_create(username='deleted_user')[0]


def deleted_userprofile():
    return UserProfile.objects.get_or_create(user=deleted_user())[0]


class Review(models.Model):
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    user = models.ForeignKey('UserProfile',
                             on_delete=models.SET_NULL,  # models.SET(deleted_userprofile),
                             null=True)
    overall_rating = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    atmosphere_rating = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    price_rating = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    service_rating = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    comment = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(null=True)#,default=datetime.datetime.now())
    picture = models.ImageField()

    def save(self, *args, **kwargs):
        self.time = datetime.datetime.now()
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        if self.user is not None:
            u = str(self.user.user.username)
        else:
            u = 'deleted'
        return str(self.page) + " | " + u + " | " + self.comment





