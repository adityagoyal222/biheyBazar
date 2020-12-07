from django.test import TestCase
import pytest
from django.urls import reverse

# Create your tests here.
@pytest.mark.django_db
def test_user_detail(client, create_user):
    user = create_user(username="test_admin")
    url = reverse('vendors:profile', kwargs={'slug': user.username})
    response = client.get(url)
    assert response.status_code == 200
    assert 'test_admin' in response.content