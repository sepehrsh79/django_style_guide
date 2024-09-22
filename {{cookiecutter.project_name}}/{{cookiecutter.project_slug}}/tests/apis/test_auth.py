import pytest
from django.test import Client
from rest_framework.test import APIClient
from django.urls import reverse
from {{cookiecutter.project_slug}}.users.models import BaseUser
import json


@pytest.mark.django_db
def test_unauth_example_api(user1, example1):
    client = Client()
    url_ = reverse("api:example:example")

    response = client.post(url_, content_type="application/json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_auth_api(api_client, user1, example1):
    url_ = reverse("api:example:example")

    response = api_client.get(url_, content_type="application/json")

    assert response.status_code == 200


@pytest.mark.django_db
def test_login(user1, example1):
    user = BaseUser.objects.create_user(
        email="js@js.com", password="js.sj"
    )

    client = APIClient()
    url_ = reverse("api:auth:jwt:login")
    body = {"email": user.email, "password": "js.sj"}
    response = client.post(url_, json.dumps(body), content_type="application/json")
    auth = json.loads(response.content)
    access = auth.get("access")
    refresh = auth.get("refresh")

    assert access != None
    assert type(access) == str

    assert refresh != None
    assert type(refresh) == str
