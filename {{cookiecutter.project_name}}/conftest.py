import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from {{cookiecutter.project_slug}}.users.models import BaseUser
from {{cookiecutter.project_slug}}.tests.factories import (
        BaseUserFactory,
        ExampleFactory,
        )


@pytest.fixture
def api_client():
    user = BaseUser.objects.create_user(email='test_user@js.com', password='pass@1test')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client

@pytest.fixture
def user1():
    return BaseUserFactory()

@pytest.fixture
def user2():
    return BaseUserFactory()

@pytest.fixture
def example1(user1):
    return ExampleFactory(author=user1)
