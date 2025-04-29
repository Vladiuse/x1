from common.request_sender import RequestSender
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import CustomUser

from links.link_content_collector import Converter, LinkContentCollector

from .models import Link, LinkCollection
from .serializers import (
    LinkCollectionManagerSerializer,
    LinkCollectionSerializer,
    LinkCreateSerializer,
    LinkReadSerializer,
)

link_content_converter = LinkContentCollector(
    request_sender=RequestSender(),
    converter=Converter(),
)


@login_required
def index(request):
    links = Link.objects.filter(owner=request.user)
    content = {
        'links': links,
    }
    return render(request, 'links/links.html', content)


class UserLinksView(ModelViewSet):
    serializer_class = LinkReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Link.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return LinkCreateSerializer
        return LinkReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        link = serializer.save()
        link_content_converter.collect(link, attempts=2)
        link.refresh_from_db()
        serializer = LinkReadSerializer(link)
        return Response(serializer.data)


class LinkCollectionView(ModelViewSet):
    serializer_class = LinkCollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LinkCollection.objects.filter(owner=self.request.user)


class LinkCollectionManagerView(APIView):
    def post(self, request, format=None):  # noqa: A002
        link, collection = self._get_link_and_collection(request=request)
        link.collections.add(collection)
        serializer = LinkReadSerializer(link)
        return Response(serializer.data)

    def delete(self, request, format=None):  # noqa: A002)
        link, collection = self._get_link_and_collection(request=request)
        link.collections.remove(collection)
        serializer = LinkReadSerializer(link)
        return Response(serializer.data)

    def _get_link_and_collection(self, request) -> tuple[Link, LinkCollection]:
        serializer = LinkCollectionManagerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        link = Link.objects.get(pk=serializer.validated_data['link_id'])
        collection = LinkCollection.objects.get(pk=serializer.validated_data['collection_id'])
        return link, collection


def users_stat(request):
    users = (
        CustomUser.objects.prefetch_related('link')
        .values('email', 'date_joined')
        .annotate(
            count=Count('link'),
            type_wesite=Count('link', filter=Q(link__type=Link.WEBSITE_TYPE)),
            type_book=Count('link', filter=Q(link__type=Link.BOOK_TYPE)),
            type_article=Count('link', filter=Q(link__type=Link.ARTICLE_TYPE)),
            type_music=Count('link', filter=Q(link__type=Link.MUSIC_TYPE)),
            type_video=Count('link', filter=Q(link__type=Link.VIDEO_TYPE)),
        )
        .order_by('-count', 'date_joined')
    )[:10]

    content = {'users': users}
    return render(request, 'links/users_stat.html', content)
