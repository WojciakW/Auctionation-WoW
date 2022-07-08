import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings
import random
from app_auctionation.models import Realms, Item
from local_credentials import USER, PASSWORD


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def realm():
    realm = random.choice(Realms.objects.all())
    return realm


@pytest.fixture
def item():
    item = random.choice(Item.objects.all())
    return item


@pytest.fixture
def faction():
    faction = random.choice(['a', 'h'])
    return faction


@pytest.fixture
def password():
    return 'test_pass'


@pytest.fixture
def create_test_user():
    user = User.objects.create_user(
        username='test_user',
        password='test_pass'
    )
    return user


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'auctionation_test',
        'HOST': '127.0.0.1',
        'USER': USER,
        'PASSWORD': PASSWORD
    }