from django.urls import path, include

urlpatterns = [
    path('example/', include(('{{cookiecutter.project_slug}}.example.urls', 'example')))
]
