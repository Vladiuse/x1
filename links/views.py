from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Link, LinkCollection
from .serializers import LinkCollectionSerializer, LinkCreateSerializer, LinkReadSerializer


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


class LinkCollectionView(ModelViewSet):
    serializer_class = LinkCollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LinkCollection.objects.filter(owner=self.request.user)
