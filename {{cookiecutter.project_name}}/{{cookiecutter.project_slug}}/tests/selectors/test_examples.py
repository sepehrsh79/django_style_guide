import pytest
from {{cookiecutter.project_slug}}.example.selectors.examples import example_list


@pytest.mark.django_db
def test_example_list(user2, user1, example1):
    a = example_list(user = user1)
    assert a.first() == example1

