import logging

import bleach
from django.views import View
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView

from feed.models import LikedFeed
from feed.serializers import FollowedFeedSerializer
from user.authentication import AppUserAuthentication
from utils.encryption import sha256
from utils.general_methods import GeneralMethods
from .models import User
from .serializers import SignUpSerializer, SignInSerializer, UserSerializer

logger = logging.getLogger(__name__)


class SignIn(CreateAPIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4>
    For user login.
    <span style='color:red'>Store token and mobile from response and send these in other APIs in headers.</span>
    </div>
    """
    serializer_class = SignInSerializer

    def create(self, request, *args, **kwargs):
        gm = GeneralMethods()
        try:
            data = gm.get_request_data(request)
            try:
                serializer = self.get_serializer(data=data)
                if not serializer.is_valid():
                    return gm.client_error_response_by_serializer(serializer.errors)
                user = User.objects.filter(is_deleted=False).get(email=data['email'])
                if user.is_blocked:
                    return gm.blocked_response()
                user.update_token()
                return gm.success_response(User.objects.filter(is_deleted=False).get(email=data['email']).login_data())
            except Exception as e:
                print(e)
                message = 'User not found'
                return gm.client_error_response(message)
        except Exception as e:
            print(e)
            logger.error(e)
            return gm.error_response()


class SignOut(RetrieveAPIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4>
    To clear user session
    </div>
    """

    def retrieve(self, request, *args, **kwargs):
        gm = GeneralMethods()
        try:
            if 'HTTP_TOKEN' not in request.META \
                    or 'HTTP_MOBILE' not in request.META:
                return gm.client_error_response('Required header missing')
            token = bleach.clean(request.META.get('HTTP_TOKEN', False))
            mobile = bleach.clean(request.META.get('HTTP_MOBILE', False))

            # Check if the data id empty or not then raise Exception
            if not token or not mobile:
                return gm.client_error_response('Invalid headers')

            user = User.objects.filter(is_deleted=False).filter(token=token).filter(mobile=mobile)
            if not user:
                return gm.client_error_response('Already logged out')
            user.get(mobile=mobile).logout()
            return gm.success_response('success')
        except Exception as e:
            print(e)
            logger.error(e)
            return gm.error_response()


class SignUp(CreateAPIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4>
    For user sign-up. <span>User will receive an OTP SMS</span>
    </div>
    """
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        gm = GeneralMethods()
        try:
            data = gm.get_request_data(request)
            try:
                serializer = self.get_serializer(data=data)
                if serializer.is_valid():
                    serializer.save(password=sha256(gm.encode(data['password'])))
                    User.objects.filter(is_deleted=False).get(email=data['email']).update_token()
                    return gm.success_response(
                        User.objects.filter(is_deleted=False).get(email=data['email']).login_data())
                else:
                    return gm.client_error_response_by_serializer(serializer.errors)
            except Exception as e:
                print(e)
                message = 'User already exists'
                return gm.client_error_response(message)
            # user = User.objects.get(Q(email=email) | Q(mobile=mobile))
        except Exception as e:
            print(e)
            logger.error(e)
            return gm.error_response()


class Profile(APIView):
    """
    <div style='border: 1px solid lightgray;padding:0.5rem; background-color:#f7f7f9'>
    <h4>Description:</h4> To display user's profile, followed events and feeds.
    </div>
    """
    gm = GeneralMethods()
    authentication_classes = [AppUserAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            mobile = bleach.clean(request.META.get('HTTP_MOBILE', ''))

            # user's profile
            user = User.objects.filter(is_deleted=False).get(mobile=mobile)
            data = dict()
            user_serializer = UserSerializer(user)
            data.update({'user': user_serializer.data})

            # Followed feeds
            followed_feed = LikedFeed.objects.filter(is_deleted=False).filter(user__id=user.pk).select_related()
            followed_feed_serializer = FollowedFeedSerializer(followed_feed, many=True)
            data.update({'following_feeds': followed_feed_serializer.data})

            return self.gm.success_response(data)
        except Exception as e:
            print(e)
            return self.gm.error_response()
