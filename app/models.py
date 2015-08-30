from django.contrib.gis.db.models import PolygonField
from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract =True

class Category(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    image = models.CharField(max_length=300)
    def __unicode__(self):
        return self.name

class Gallery(BaseModel):
    image_link = models.CharField(max_length=200)
    short_description = models.CharField(max_length=100)

class Location(BaseModel):
    area = models.CharField(max_length=100,default="",blank=True,null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    mpoly = PolygonField()

    def __unicode__(self):
        return self.city

class Place(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    image = models.CharField(max_length=200,default="")
    location = models.ForeignKey(Location,null=True)
    short_description = models.CharField(max_length=300,default="")
    duration = models.CharField(max_length=100,default="")
    budget = models.IntegerField(default=0,null=True)
    category = models.ForeignKey(Category)
    gallery = models.ManyToManyField(Gallery,default=None)
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