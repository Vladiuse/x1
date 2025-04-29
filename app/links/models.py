from django.db import models
from users.models import CustomUser


class LinkCollection(models.Model):
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='collections',
        related_query_name='collection',
    )
    name = models.CharField(
        max_length=50,
    )
    description = models.CharField(
        max_length=254,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    edited = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = ('owner', 'name')


class Link(models.Model):
    WEBSITE_TYPE = 'website'
    BOOK_TYPE = 'book'
    ARTICLE_TYPE = 'article'
    MUSIC_TYPE = 'music'
    VIDEO_TYPE = 'video'

    LOAD_STATUS_LOADED = 'loaded'
    LOAD_STATUS_NOT_LOADED = 'not_loaded'
    LOAD_STATUS_ERROR = 'error'

    LINK_TYPES = [WEBSITE_TYPE, BOOK_TYPE, ARTICLE_TYPE, MUSIC_TYPE, VIDEO_TYPE]

    LOAD_STATUSES = (
        (LOAD_STATUS_LOADED, LOAD_STATUS_LOADED),
        (LOAD_STATUS_NOT_LOADED, LOAD_STATUS_NOT_LOADED),
        (LOAD_STATUS_ERROR, LOAD_STATUS_ERROR),
    )
    PAGE_TYPES = (
        (WEBSITE_TYPE, WEBSITE_TYPE),
        (BOOK_TYPE, BOOK_TYPE),
        (ARTICLE_TYPE, ARTICLE_TYPE),
        (MUSIC_TYPE, MUSIC_TYPE),
        (VIDEO_TYPE, VIDEO_TYPE),
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='links',
        related_query_name='link',
    )
    url = models.URLField()
    parsed_url = models.CharField(
        max_length=254,
        blank=True,
        null=True,
        default=None,
    )
    title = models.CharField(
        max_length=254,
        blank=True,
        null=True,
        default=None,
    )
    description = models.TextField(
        blank=True,
        null=True,
        default=None,
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        default=None,
    )
    type = models.CharField(
        max_length=60,
        blank=True,
        choices=PAGE_TYPES,
        null=True,
        default=None,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    edited = models.DateTimeField(
        auto_now=True,
    )
    collections = models.ManyToManyField(
        LinkCollection,
        related_name='links',
        related_query_name='link',
        blank=True,
    )
    load_status = models.CharField(
        max_length=20,
        choices=LOAD_STATUSES,
        default=LOAD_STATUS_NOT_LOADED,
    )

    class Meta:
        unique_together = ('owner', 'url')


def normalize_link_type(link_type: str | None) -> str:
    if link_type is None:
        return Link.WEBSITE_TYPE
    link_type = link_type.lower()
    if '.' in link_type:
        link_type = link_type.split('.')[0]
    return link_type if link_type in Link.LINK_TYPES else Link.WEBSITE_TYPE
