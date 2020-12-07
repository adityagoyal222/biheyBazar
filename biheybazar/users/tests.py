from django.test import TestCase
import pytest
from .models import User
from customers.models import Customer
from vendors.models import Vendor
from django.urls import reverse

# Create your tests here.
@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'softwarica')
    assert User.objects.count() == 1
