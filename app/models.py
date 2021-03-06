from django.contrib.gis.db.models import PolygonField
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract =True

class Gallery(BaseModel):
    image_link = models.CharField(max_length=200)
    short_description = models.CharField(max_length=100)

class Location(BaseModel):
    area = models.CharField(max_length=100,default="")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    mpoly = PolygonField()

    def __unicode__(self):
        return self.city

class Category(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    image = models.CharField(max_length=300)
    location = models.ManyToManyField(Location,null=True,blank=True)

    def __unicode__(self):
        return self.name

class Highlight(BaseModel):
    highlight_text = models.CharField(max_length=200)
    
class Place(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    image = models.CharField(max_length=200,default="")
    location = models.ForeignKey(Location,null=True,blank=True)
    short_description = models.CharField(max_length=300,default="")
    duration = models.CharField(max_length=100,default="")
    budget = models.IntegerField(default=0,null=True)
    category = models.ForeignKey(Category)
    gallery = models.ManyToManyField(Gallery,default=None)
    highlight = models.ManyToManyField(Highlight,blank=True,null=True)
    def __unicode__(self):
        return self.name

class Description(BaseModel):
    text = models.TextField()
    heading = models.CharField(max_length=100)
    place = models.ForeignKey(Place,null=True)

class Visitor(BaseModel):
    app_id = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    app_version = models.CharField(max_length=10)

class HotPlaces(BaseModel):
    place = models.ForeignKey(Place)
    image = models.CharField(max_length=100,default="")

class UserProfile(BaseModel):
    user = models.OneToOneField(User)
    app_id = models.CharField(max_length=200)

class Rating(BaseModel):
    place = models.ForeignKey(Place)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=0)

class Booking(BaseModel):
    place = models.ForeignKey(Place)
    user = models.ForeignKey(UserProfile)
    date_of_booking = models.DateTimeField(blank=True,null=True)