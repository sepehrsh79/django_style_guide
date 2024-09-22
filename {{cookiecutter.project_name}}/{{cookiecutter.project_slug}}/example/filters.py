from django_filters import (
    CharFilter,
    FilterSet,
)
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from {{cookiecutter.project_slug}}.example.models import Example
from rest_framework.exceptions import APIException


class ExampleFilter(FilterSet):
    search = CharFilter(method="filter_search")
    user__in = CharFilter(method="filter_user__in")
    created_at__range = CharFilter(method="filter_created_at__range")

    def filter_user__in(self, queryset, name, value):
        limit = 10
        users = value.split(",")
        if len(users) > limit:
            raise APIException(f"You cannot add more than {len(users)} usernames")
        return queryset.filter(user__email__in=users)

    def filter_created_at__range(self, queryset, name, value):
        limit = 2
        created_at__in = value.split(",")
        if len(created_at__in) > limit:
            raise APIException("Please just add two created_at with , in the middle")

        created_at_0, created_at_1 = created_at__in

        if not created_at_1:
            created_at_1 = timezone.now()

        if not created_at_0:
            return queryset.filter(created_at__date__lt=created_at_1)

        return queryset.filter(created_at__date__range=(created_at_0, created_at_1))

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("title")).filter(search=value)

    class Meta:
        model = Example
        fields = (
            "slug",
            "title",
        )
