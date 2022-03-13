import factory
from factory.faker import faker
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

fake = faker.Faker()

class AccountFactory(factory.django.DjangoModelFactory):
    email = 'test@gmail.com'
    username = "test"
    full_name = 'test account'
    date_of_birth = fake.date()
    hide_email = False
    

    class Meta:
        model = Account