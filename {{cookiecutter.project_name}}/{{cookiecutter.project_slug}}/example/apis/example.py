from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from {{cookiecutter.project_slug}}.api.pagination import  get_paginated_response, LimitOffsetPagination, get_paginated_response_context
from rest_framework.pagination import PageNumberPagination

from {{cookiecutter.project_slug}}.example.models import Example
from {{cookiecutter.project_slug}}.example.selectors.examples import example_detail, example_list 
from {{cookiecutter.project_slug}}.example.services.example import create_example 
from {{cookiecutter.project_slug}}.api.mixins import ApiAuthMixin


class ExampleApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, max_length=100)
        search = serializers.CharField(required=False, max_length=100)
        created_at__range= serializers.CharField(required=False, max_length=100)
        user__in= serializers.CharField(required=False, max_length=100)
        slug = serializers.CharField(required=False, max_length=100)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)

    class OutPutSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Example
            fields = ("url", "title", "user")

        def get_user(self, example):
            return example.author.email

        def get_url(self, example):
            request = self.context.get("request")
            path = reverse("api:example:example_detail", args=(example.slug,))
            return request.build_absolute_uri(path)

    @extend_schema(
        responses=OutPutSerializer,
        request=InputSerializer,
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = create_example(
                user=request.user,
                content=serializer.validated_data.get("content"),
                title=serializer.validated_data.get("title"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutSerializer(query, context={"request":request}).data)

    @extend_schema(
        parameters=[FilterSerializer],
        responses=OutPutSerializer,
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            query = example_list(filters=filters_serializer.validated_data, user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class ExampleDetailApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutPutDetailSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_user")

        class Meta:
            model = Example
            fields = ("user", "slug", "title", "created_at", "updated_at")

        def get_user(self, example):
            return example.user.email


    @extend_schema(
        responses=OutPutDetailSerializer,
    )
    def get(self, request, slug):

        try:
            query = example_detail(slug=slug, user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.OutPutDetailSerializer(query)

        return Response(serializer.data) 
