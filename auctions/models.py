from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.sessions.models import Session



User = settings.AUTH_USER_MODEL

class User(AbstractUser):
    pass

class AL(models.Model):
    
    favourites = models.ManyToManyField(User, related_name ='favourite', default=None)
    current_price = models.PositiveIntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.URLField() 
    title=models.CharField(max_length=100)
    timestamp = models.DateTimeField(default = timezone.now)
    category = models.CharField(max_length=100)
    contacts= models.PositiveIntegerField(default = 0)
    description=models.TextField()
    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.username, self.category, self.title, self.timestamp, self.favourites, self.img, self.id)
    def get_absolute_url(self):
        return reverse("al_detail", kwargs={'pk':self.pk})

class Bid(models.Model):
    io = models.BooleanField(default = False)
    y = models.IntegerField(default= None)
    username  = models.ForeignKey(User, on_delete=models.CASCADE)
    current_bid = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return '{} {} {} {}'.format(self.username, self.current_bid, self.y, self.io)
class Comment(models.Model):
    i = models.IntegerField(default= None)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.TextField(default= None)
    timestamp = models.DateTimeField(default = timezone.now)
class Close_Bid(models.Model):
    y = models.IntegerField(default= None)
    img = models.URLField(default= None) 
    title = models.CharField(max_length=100, default=None) 
    io = models.BooleanField(default = False)
    username  = models.ForeignKey(User, on_delete=models.CASCADE)
    current_bid = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return '{} {} {} {}'.format(self.username, self.current_bid, self.y, self.io)



