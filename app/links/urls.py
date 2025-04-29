from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('links', views.UserLinksView, basename='userlinks')
router.register('link-collections', views.LinkCollectionView, basename='linkcollections')

app_name = 'links'

urlpatterns = [
    path('', views.index, name='index'),
    path('link-collection-manager/', views.LinkCollectionManagerView.as_view(), name='link_collection_manager'),
]
urlpatterns += router.urls
