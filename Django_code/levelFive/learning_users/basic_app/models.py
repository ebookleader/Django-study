from django.db import models
from django.contrib.auth.models import User
# default user already has things like email, password, first name etc

# Create your models here.

class UserProfileInfo(models.Model):
    
    #if you want to add more attributes to your actual user
    #you can extend the class of this one to one relationship
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    # additional
    # there's not goint to be an error if they don't provide it

    portfolio_site = models.URLField(blank=True)
    # profile_pics is a subdirectory
    # when people upload their images, they are going to be saved profile_pics under media
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    # when working with images, we have to install pillow library

    def __str__(self):
        return self.user.username
