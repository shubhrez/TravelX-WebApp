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

class Image(BaseModel):
    link = models.CharField(max_length=200)
    short_description = models.CharField(max_length=100)

class Location(BaseModel):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class Place(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    images = models.ManyToManyField(Image)
    location = models.ForeignKey(Location)
    description = models.CharField(max_length=300)
    duration = models.IntegerField(default=0,null=True)
    budget = models.IntegerField(default=0,null=True)

