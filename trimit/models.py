from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from geopy.geocoders import GoogleV3
import datetime
from TeamI.settings import GoogleGeocodeKey
from django.conf import settings
from django.db.models import Avg
import tagulous.models
from TeamI.settings import STATIC_URL

API_KEY = GoogleGeocodeKey
HAIRDRESSER_GROUP = 'hairdressers'
USER_GROUP = 'users'

User = settings.AUTH_USER_MODEL

# class EUser(AbstractUser):
#     email = models.EmailField(unique=True, blank=False)

class Specialities(tagulous.models.TagModel):
    class TagMeta:
        space_delimiter = False
        force_lowercase = True
        # autocomplete_limit = 8
        verbose_name_singular = 'Speciality'
        verbose_name_plural = 'Specialities'


class Page(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='Page')
    specialities = tagulous.models.TagField(to=Specialities, blank=True)
    profile_picture = models.ImageField(upload_to='user_profile_images', default='DefaultPagePic.png', blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    # Contact Info
    flat_number = models.CharField(max_length=15, blank=True)
    street_address = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    postcode = models.CharField(max_length=30, blank=True)
    country = CountryField(blank=False)
    opening_times = models.CharField(max_length=200, blank=True, null=True)
    webpage = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    # Ratings
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, null=True)
    mean_atmosphere_rating = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    mean_price_rating = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    mean_service_rating = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    number_of_reviews = models.DecimalField(max_digits=5, decimal_places=0, default=0, null=True)

    # Map Location
    latitude = models.DecimalField(decimal_places=5, max_digits=9, blank=True, null=True, default=None)
    longitude = models.DecimalField(decimal_places=5, max_digits=9, blank=True, null=True, default=None)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        group = Group.objects.get_or_create(name=HAIRDRESSER_GROUP)[0]
        self.user.groups.add(group)
        spaced_name = self.user.username
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

    def update_overall_rating(self):
        print("Updating {} reviews by adding new one..".format(self.name))
        own_reviews = Review.objects.filter(page__slug=self.slug)
        self.number_of_reviews = len(own_reviews)

        sum_atmosphere_rating = 0
        sum_price_rating = 0
        sum_service_rating = 0
        for i in own_reviews:
            sum_atmosphere_rating += i.atmosphere_rating
            sum_price_rating += i.price_rating
            sum_service_rating += i.service_rating

        self.mean_atmosphere_rating = sum_atmosphere_rating / self.number_of_reviews 
        self.mean_price_rating = sum_price_rating / self.number_of_reviews 
        self.mean_service_rating = sum_service_rating / self.number_of_reviews
        self.overall_rating = (self.mean_atmosphere_rating + self.mean_price_rating + 
                               self.mean_service_rating) / 3 

        super(Page, self).save()
        

    def __str__(self):
        return self.user.username

    @property
    def avgp(self):
        return Review.objects.filter(page=self).aggregate(Avg('price_rating'))['price_rating__avg']

    @property
    def avgs(self):
        return Review.objects.filter(page=self).aggregate(Avg('service_rating'))['service_rating__avg']

    @property
    def avga(self):
        return Review.objects.filter(page=self).aggregate(Avg('atmosphere_rating'))['atmosphere_rating__avg']

    @property
    def avgo(self):
        return Review.objects.filter(page=self).aggregate(Avg('overall_rating'))['overall_rating__avg']

class Treatment(models.Model):
    page = models.ForeignKey('Page',
                             on_delete=models.CASCADE,
                             related_name='page')
    description = models.CharField(max_length=50)
    price = models.CharField(max_length=150)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    profile_picture = models.ImageField(upload_to='user_profile_images', default='DefaultUserPic.png', blank=True)
    favourites = models.ManyToManyField(to='Page', related_name='favourited')
   # hairpicture = models.ImageField(upload_to='user_images', blank=True)

    def save(self, *args, **kwargs):
        group = Group.objects.get_or_create(name=USER_GROUP)[0]
        self.user.groups.add(group)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


def deleted_user():
    return get_user_model().objects.get_or_create(username='deleted_user')[0]


def deleted_userprofile():
    return UserProfile.objects.get_or_create(user=deleted_user())[0]


class Review(models.Model):
    page = models.ForeignKey('Page',
                             on_delete=models.CASCADE,
                             related_name='reviews')
    user = models.ForeignKey('UserProfile',
                             on_delete=models.SET_NULL,  # models.SET(deleted_userprofile),
                             null=True,
                             related_name='reviews')
    average_rating = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    atmosphere_rating = models.DecimalField(max_digits=10, decimal_places=1)
    price_rating = models.DecimalField(max_digits=10, decimal_places=1)
    service_rating = models.DecimalField(max_digits=10, decimal_places=1)
    comment = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(null=True)#,default=datetime.datetime.now())
    picture = models.ImageField(upload_to='review_images', blank=True)

    def save(self, *args, **kwargs):
        all_ratings = [self.atmosphere_rating, self.price_rating, self.service_rating]
        self.average_rating = sum([i for i in all_ratings if i if not None])/3
        self.time = datetime.datetime.now()
        super(Review, self).save(*args, **kwargs)
        self.page.update_overall_rating()

    def __str__(self):
        if self.user is not None:
            u = str(self.user.user.username)
        else:
            u = 'deleted'
        return str(self.id) + ' | ' + str(self.page) + " | " + u + " | " + self.comment


class PageImage(models.Model):
    image = models.ImageField(upload_to='hairpage_images', blank=False)
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='images')
    text = models.CharField(max_length=140, blank=True)
    upload_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.upload_time = datetime.datetime.now()
        super(PageImage, self).save(*args, **kwargs)

    def __str__(self):
        return 'image ' + str(self.id) + ' ' + str(self.page) + ' ' + str(self.upload_time.date())


class UserHairImage(models.Model):
    image = models.ImageField(upload_to='user_hair_images', blank=False)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='images')
    text = models.CharField(max_length=140, blank=True)
    upload_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.upload_time = datetime.datetime.now()
        super(UserHairImage, self).save(*args, **kwargs)

    def __str__(self):
        return 'image ' + str(self.id) + ' ' + str(self.user) + ' ' + str(self.upload_time.date())

