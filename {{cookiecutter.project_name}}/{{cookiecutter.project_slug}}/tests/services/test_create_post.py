import pytest
from {{cookiecutter.project_slug}}.example.services.example import create_example


@pytest.mark.django_db
def test_create_example(user2, user1, example1):
    a = create_example(user = user1, title="pooo", description="CCCContent")

    assert a.user == user1
    assert a.title == "pooo"
    assert a.description == "CCCContent"
