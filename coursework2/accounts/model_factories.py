import factory
from factory.faker import faker
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

fake = faker.Faker()

class AccountFactory(factory.django.DjangoModelFactory):
    email = faker.ascii_email()
    username = "test"
    full_name = fake.name()
    date_of_birth = faker.date()

    class Meta:
        model = Account