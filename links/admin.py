from django.contrib import admin
from .models import Link, LinkCollection


class LinkCollectionAdmin(admin.ModelAdmin):

    list_display = ['pk', 'owner', 'name']

admin.site.register(LinkCollection, LinkCollectionAdmin)

