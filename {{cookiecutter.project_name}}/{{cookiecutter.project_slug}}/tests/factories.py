import factory

from {{cookiecutter.project_slug}}.tests.utils import faker
from {{cookiecutter.project_slug}}.users.models import BaseUser
from {{cookiecutter.project_slug}}.example.models import Example
       
from django.utils import timezone


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    email    = factory.Iterator(['fr@gmail.com', 'it@gmail.com', 'es@gmail.com'])
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')


class ExampleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Example

    title   = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    content = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    slug    = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    created_at           = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    updated_at           = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    author = factory.SubFactory(BaseUserFactory)
