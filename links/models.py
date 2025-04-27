from django.db import models

from users.models import CustomUser


class LinkCollection(models.Model):
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='collections',
        related_query_name='collection',
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=254, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'name')


class Link(models.Model):
    WEBSITE_TYPE = 'website'
    BOOK_TYPE = 'book'
    ARTICLE_TYPE = 'article'
    MUSIC_TYPE = 'music'
    VIDEO_TYPE = 'video'

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
    title = models.CharField(max_length=254, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    type = models.CharField(max_length=20, blank=True, choices=PAGE_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    collections = models.ManyToManyField(LinkCollection, related_name='links', related_query_name='link')

    class Meta:
        unique_together = ('owner', 'url')
