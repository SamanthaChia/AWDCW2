from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class AccountManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None):
        if not email:
            raise ValueError('An account needs an email address')
        if not username:
            raise ValueError('An account needs a username')
        if not full_name:
            raise ValueError('An account needs a name')

        email = self.normalize_email(email)    
        user = self.model(
            email = email,
            username = username,
            full_name = full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            full_name = full_name,
            password=password,
        )
        
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
        
# profile_images file will be saved in media_cdn separated by pk of user
def get_profile_image(self, filename):
    return 'profile_images/'+ str(self.pk) + '/"profile_image.png"'

def get_default_profile_image():
    return "defaultImgs/default_profile_image.jpg"


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=256, unique=True)
    username = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=256)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=256, upload_to=get_profile_image, null=True, blank=True, default=get_default_profile_image)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    hide_email = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True