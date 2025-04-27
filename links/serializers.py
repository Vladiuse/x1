from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from .models import Link, LinkCollection


class LinkCollectionSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        internal_data = super().to_internal_value(data)
        internal_data['owner'] = self.context['request'].user
        return internal_data

    class Meta:
        model = LinkCollection
        fields = '__all__'
        read_only_fields = ('owner', 'created', 'edited')
        validators = [
            UniqueTogetherValidator(
                queryset=LinkCollection.objects.all(),
                fields=['owner', 'url'],
            ),
        ]


class LinkReadSerializer(serializers.ModelSerializer):
    # collections = LinkCollectionSerializer(many=True)

    class Meta:
        model = Link
        fields = '__all__'


class LinkCreateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        internal_data = super().to_internal_value(data)
        internal_data['owner'] = self.context['request'].user
        return internal_data

    def validate_collections(self, value: list[int]) -> list[int]:
        not_owner_link_collection_ids = set()
        for collection in value:
            if collection.owner_id != self.context['request'].user.pk:
                not_owner_link_collection_ids.add(collection.pk)
        if len(not_owner_link_collection_ids) > 0:
            raise ValidationError(
                f'You cant add link in not yours collection! Wronge ids: {not_owner_link_collection_ids}',
            )
        return value

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ('owner', 'created', 'edited', 'title', 'description', 'image_url', 'type')
        validators = [
            UniqueTogetherValidator(
                queryset=Link.objects.all(),
                fields=['owner', 'url'],
            ),
        ]
