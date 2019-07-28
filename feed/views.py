import bleach
from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
import logging
from feed.models import Feed, LikedFeed, FavouriteFeed
from feed.serializers import FeedSerializer
from user.authentication import AppUserAuthentication
from user.models import User
from utils.general_methods import GeneralMethods

logger = logging.getLogger(__name__)


class FeedList(ListAPIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4> Return a list of all the existing feeds.
    For Pagination append this in URL (default list of  objects is 20)
    <span style='color: red'>(?page=2)</span>
    </div>
    """
    authentication_classes = [AppUserAuthentication]
    serializer_class = FeedSerializer
    queryset = Feed.objects.filter(is_deleted=False).all().select_related()
    gm = GeneralMethods()

    def list(self, request, *args, **kwargs):
        queryset = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = self.get_paginated_response(serializer.data)
        mobile = bleach.clean(request.META.get('HTTP_MOBILE', ''))
        feeds_id_list = [row['id'] for row in data['results']]
        liked_feeds = LikedFeed.objects.filter(is_deleted=False).filter(id__in=feeds_id_list).filter(
            user__pk=User.objects.get(mobile=mobile).pk)
        feeds_liked_by_me = [row.feed.id for row in liked_feeds]
        for row in data['results']:
            row.update({'liked_by_me': True if row['id'] in feeds_liked_by_me else False})
        return self.gm.success_response(data)


class FeedDetails(RetrieveAPIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4> Return an of the existing feed by it's id.
    </div>
    """
    authentication_classes = [AppUserAuthentication]
    serializer_class = FeedSerializer
    lookup_field = 'id'
    queryset = Feed.objects.filter(is_deleted=False).all()
    gm = GeneralMethods()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict()
        data.update(serializer.data)
        mobile = bleach.clean(request.META.get('HTTP_MOBILE', ''))
        user = User.objects.get(mobile=mobile)
        liked_feed = LikedFeed.objects.filter(is_deleted=False).filter(feed__pk=data['id'])
        if liked_feed and liked_feed.get(feed__pk=data['id']).user.pk == user.pk:
            data.update({'liked_by_me': True})
        else:
            data.update({'liked_by_me': False})
        return self.gm.success_response(serializer.data)

    def handle_exception(self, exc):
        """
        If `request.method` does not correspond to a handler method,
        determine what kind of exception to raise.
        """
        return self.gm.client_error_response('No feed found')


class FeedLiked(APIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4> To like or undo-like an feed.
    </div>
    """
    authentication_classes = [AppUserAuthentication]
    gm = GeneralMethods()

    def get(self, request, *args, **kwargs):
        try:
            mobile = bleach.clean(request.META.get('HTTP_MOBILE', ''))
            user = User.objects.filter(is_deleted=False).get(mobile=mobile)
            feed_id = kwargs.get('id', '')
            if not feed_id:
                return self.gm.client_error_response('Feed Id is required')

            feed_exists = Feed.objects.filter(is_deleted=False).filter(id=feed_id)
            if not feed_exists:
                return self.gm.client_error_response('Invalid feed id')
            feed = feed_exists.get(id=feed_id)
            # # Check if already exists or not
            # # If exists, deleted it.
            already_liked = LikedFeed.objects.filter(is_deleted=False).filter(user__id=user.id).filter(feed__id=feed.id)
            if already_liked:
                already_liked.update(is_deleted=True)
                Feed.objects.filter(is_deleted=False).filter(id=feed_id).update(likes=F('likes') - 1)
                return self.gm.success_response('disliked')
            else:
                LikedFeed.objects.create(
                    user=user,
                    feed=feed
                )
                Feed.objects.filter(is_deleted=False).filter(id=feed_id).update(likes=F('likes') + 1)
                return self.gm.success_response('liked')
        except Exception as e:
            print(e)
            logger.error(e)
            return self.gm.error_response()

    def handle_exception(self, exc):
        """
        If `request.method` does not correspond to a handler method,
        determine what kind of exception to raise.
        """
        return self.gm.client_error_response('No feed found')


class FeedFavourite(APIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4> To add a feed as a favourite or remove favourite feed.
    </div>
    """
    authentication_classes = [AppUserAuthentication]
    gm = GeneralMethods()

    def get(self, request, *args, **kwargs):
        try:
            mobile = bleach.clean(request.META.get('HTTP_MOBILE', ''))
            user = User.objects.filter(is_deleted=False).get(mobile=mobile)
            feed_id = kwargs.get('id', '')
            if not feed_id:
                return self.gm.client_error_response('Feed Id is required')

            feed_exists = Feed.objects.filter(is_deleted=False).filter(id=feed_id)
            if not feed_exists:
                return self.gm.client_error_response('Invalid feed id')
            feed = feed_exists.get(id=feed_id)
            # # Check if already exists or not
            # # If exists, deleted it.
            already_exists = FavouriteFeed.objects.filter(is_deleted=False).filter(user__id=user.id).filter(
                feed__id=feed.id)
            if already_exists:
                already_exists.update(is_deleted=True)
                return self.gm.success_response('Favourite removed')
            else:
                FavouriteFeed.objects.create(
                    user=user,
                    feed=feed
                )
                return self.gm.success_response('Favourite added')
        except Exception as e:
            print(e)
            logger.error(e)
            return self.gm.error_response()

    def handle_exception(self, exc):
        """
        If `request.method` does not correspond to a handler method,
        determine what kind of exception to raise.
        """
        return self.gm.client_error_response('No feed found')
