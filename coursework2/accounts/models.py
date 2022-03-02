from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# profile_images file will be saved in media_cdn separated by pk of user
def get_profile_image(self):
    return 'profile_images/'+ self.pk + '/"profile_image.png"'

def get_default_profile_image():
    return "defaultImgs/default_profile_image.jpg"

# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(max_length=256, upload_to=get_profile_image, null=True, blank=True, default=get_default_profile_image)
    hide_phone = models.BooleanField(default=True)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    # Retrieve 
    def get_name(self):
        return self.name

    def get_username(self):
        return self.username

    def get_user_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/'+self.pk+'/'):]