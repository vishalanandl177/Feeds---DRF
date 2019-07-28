from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN

from config.constant import UNAUTHORIZED, SESSION_EXPIRED, ERROR_STATUS_CODE, \
    NOT_ACCEPTABLE, BAD_REQUEST, INTERNAL_SERVER_ERROR, INSUFFICIENT_HEADERS, \
    BLOCKED_CLIENT_MESSAGE, NO_USER_FOUND, FORBIDDEN


class ServerException(APIException):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    default_code = INTERNAL_SERVER_ERROR

    def __init__(self):
        self.detail = {'status': ERROR_STATUS_CODE, 'result': INTERNAL_SERVER_ERROR}


class UnauthorizedException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_code = UNAUTHORIZED

    def __init__(self):
        self.detail = {'status': ERROR_STATUS_CODE, 'result': UNAUTHORIZED}


class SessionExpiredException(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_code = FORBIDDEN

    def __init__(self):
        self.detail = {'status': ERROR_STATUS_CODE, 'result': SESSION_EXPIRED}


class MissingHeaderException(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_code = BAD_REQUEST

    def __init__(self):
        self.detail = {'status': ERROR_STATUS_CODE, 'result': INSUFFICIENT_HEADERS}


class BlockedClientException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_code = UNAUTHORIZED

    def __init__(self):
        self.detail = {'status': ERROR_STATUS_CODE, 'result': BLOCKED_CLIENT_MESSAGE}


class UserNotFoundException(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_code = UNAUTHORIZED

    def __init__(self):
        self.detail = {'status': ERROR_STATUS_CODE, 'result': NO_USER_FOUND}
