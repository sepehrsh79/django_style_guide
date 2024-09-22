from django.urls import path

from {{cookiecutter.project_slug}}.apis.example import ExampleApi, ExampleDetailApi


app_name = "example"
urlpatterns = [
        path("example/", ExampleApi.as_view(), name="example"),
        path("example/<slug:slug>", ExampleDetailApi.as_view(), name="example_detail"),
        ]

