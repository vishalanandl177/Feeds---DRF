from rest_framework import serializers
from . import models


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Feed
        fields = ('id', 'title', 'user', 'description', 'tags', 'image', 'likes',)


class FollowedFeedSerializer(serializers.ModelSerializer):
    feed = FeedSerializer()

    class Meta:
        model = models.Feed
        fields = ('id', 'feed',)


