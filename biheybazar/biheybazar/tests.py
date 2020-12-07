from django.urls import reverse
import pytest
import uuid

@pytest.mark.django_db
def test_home_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.fixture
def test_password():
    return 'softwarica'


@pytest.fixture
def create_customer(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        kwargs['is_customer'] = True
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user