from django.contrib import admin
from .models import Link, LinkCollection


class LinkAdmin(admin.ModelAdmin):

    list_display = ['pk', 'owner', 'url', 'title', 'description', 'image_url', 'type', 'created', 'load_status']

class LinkCollectionAdmin(admin.ModelAdmin):

    list_display = ['pk', 'owner', 'name']

admin.site.register(Link, LinkAdmin)
admin.site.register(LinkCollection, LinkCollectionAdmin)

