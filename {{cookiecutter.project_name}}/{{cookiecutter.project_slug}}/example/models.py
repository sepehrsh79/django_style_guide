from django.db import models
from django.core.exceptions import ValidationError
from {{cookiecutter.project_slug}}.common.models import BaseModel
from {{cookiecutter.project_slug}}.users.models import BaseUser


class Example(BaseModel):

    slug = models.SlugField(
            primary_key=True,
            max_length=100,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
    )
    description = models.TextField()
    user = models.ForeignKey(
            BaseUser, 
            on_delete=models.SET_NULL,
            null=True,
    )

    def __str__(self):
        return self.slug

