from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# profile_images file will be saved in media_cdn separated by pk of user
def get_profile_image(self):
    return 'profile_images/'+ self.pk + '/"profile_image.png"'

def get_default_profile_image():
    return "logo here"

# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(max_length=256, upload_to=get_profile_image, null=True, blank=True, default=get_default_profile_image)
