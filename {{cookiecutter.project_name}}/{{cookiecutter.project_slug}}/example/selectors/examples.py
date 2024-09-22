from django.db.models import QuerySet
from {{cookiecutter.project_slug}}.example.models import Example
from {{cookiecutter.project_slug}}.users.models import BaseUser
from {{cookiecutter.project_slug}}.example.filters import ExampleFilter

def example_detail(*, slug:str, user_id:BaseUser) -> Example:
    users = list(BaseUser.objects.filter(id=user_id).values_list("target", flat=True))
    return Example.objects.get(slug=slug, user__in=users)

def example_list(*, filters=None, user_id:BaseUser) -> QuerySet[Example]:
    filters = filters or {}
    users = list(BaseUser.objects.filter(id=user_id).values_list("target", flat=True))
    if users:
        qs = Example.objects.filter(user__in=users)
        return ExampleFilter(filters, qs).qs
    return Example.objects.none()

