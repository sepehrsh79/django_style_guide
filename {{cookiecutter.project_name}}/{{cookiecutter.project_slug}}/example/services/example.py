from django.db.models import QuerySet
from {{cookiecutter.project_slug}}.example.models import Example


def create_example(*, title: str) -> QuerySet[Example]:
    return Example.objects.create(title=title)
