from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django import forms


class User(AbstractUser):
    pass
    def __str__(self):
            return f"{self.first_name} {self.last_name}"

class Categories(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting = models.IntegerField()
    image = models.ImageField(upload_to="image",editable=True,blank=True)
    is_close = models.BooleanField(default=False,editable=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,blank=True,related_name="categories")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="listings")
    watchlist = models.ManyToManyField(User,blank=True,related_name="watchlist")
    
    def __str__(self):
        return f"{self.title} (by {self.user})"
    
class Bid(models.Model):
    price = models.IntegerField()
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="listingbids")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userbids")
    
    def __str__(self):
        return f"{self.price} (by {self.user})"


class Comment(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comments")
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="usercomment")

    def __str__(self):
        return f"{self.text} (by {self.user})"
    


