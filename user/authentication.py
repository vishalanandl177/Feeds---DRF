from django.utils import timezone
from rest_framework import authentication

from config.base_settings import APP_USER_SESSION_EXPIRE_DAY_COUNT
from utils.exceptions import MissingHeaderException, UnauthorizedException, \
    BlockedClientException
import bleach
from user.models import User


class AppUserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        # make sure token, username and short code exists in headers
        if 'HTTP_TOKEN' not in request.META \
                or 'HTTP_MOBILE' not in request.META:
            raise MissingHeaderException()
        token = bleach.clean(request.META.get('HTTP_TOKEN', ''))
        mobile = bleach.clean(request.META.get('HTTP_MOBILE', ''))

        # Check if the data id empty or not then raise Exception
        if not token or not mobile:
            raise MissingHeaderException()

        # Check if the session exists or not
        try:
            user = User.objects.filter(is_deleted=False).filter(token=token) \
                .filter(token_expire_on__gt=timezone.now()).get(mobile=mobile)
            if user.is_blocked:
                raise BlockedClientException()
            User.objects.filter(mobile=mobile).update(
                token_expire_on=timezone.now() + timezone.timedelta(days=APP_USER_SESSION_EXPIRE_DAY_COUNT))
        except Exception as e:
            print(e)
            raise UnauthorizedException()

        # If valid return None
        return None
