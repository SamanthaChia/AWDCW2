from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# profile_images file will be saved in media_cdn separated by pk of user
def get_profile_image(self):
    return 'profile_images/'+ self.pk + '/"profile_image.png"'

def get_default_profile_image():
    return "defaultImgs/default_profile_image.jpg"

class AccountManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('An account needs an email address')
        if not username:
            raise ValueError('An account needs a username')
        if not full_name:
            raise ValueError('An account needs a name')
            
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            full_name = full_name,
            **extra_fields
        )

        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password=None, **extra_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            full_name = full_name,
            **extra_fields
        )
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=256, upload_to=get_profile_image, null=True, blank=True, default=get_default_profile_image)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    hide_phone = models.BooleanField(default=True)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username']

    objects = AccountManager()

    # Retrieve 
    def get_fullname(self):
        return self.full_name

    def get_username(self):
        return self.username

    def get_user_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/'+self.pk+'/'):]

    def has_permission(self, perm, obj=None):
        return self.is_admin

    def has_module_permission(self, app_label):
        return True