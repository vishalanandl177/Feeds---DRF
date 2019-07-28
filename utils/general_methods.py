import re
import base64
from rest_framework.response import Response
import json
import hashlib

from rest_framework.status import HTTP_400_BAD_REQUEST, \
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_406_NOT_ACCEPTABLE
import logging
from config.constant import ERROR_STATUS_CODE, SUCCESS_STATUS_CODE, INTERNAL_SERVER_ERROR_CLIENT_MESSAGE
from config.settings import SECRET_KEY, WEB_USER_SESSION_EXPIRE_DAY_COUNT, BLOCKED_CLIENT_MESSAGE

logger = logging.getLogger(__name__)


class GeneralMethods:

    def __init__(self):
        pass

    """
        Function:       get_request_data(self, request)
        Description:    To get the jso data from request
    """

    def get_request_data(self, request):
        try:
            return request.data
        except:
            return json.loads(request.body.decode("utf-8"))

    """
        Function:       error_log(self, api_view, message)
        Description:    To log the errors
        Input:          api_view name and errors
    """

    def error_log(self, api_view, message):
        logger.error(str(api_view) + ' - ' + str(message))

    """
        Function:       warning_log(self, api_view, message)
        Description:    To log the warnings
        Input:          api_view name and warnings
    """

    def warning_log(self, api_view, message):
        logger.warning(str(api_view) + ' - ' + str(message))

    def log(self, info):
        logger.debug(info)

    def get_client_ip(self, request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        except:
            return False

    def is_valid_email(self, email):
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            return False
        return True

    def is_string_and_number(self, data, with_space=True):
        # Includes space also
        regex = '^[ a-zA-Z0-9]+$'
        if not with_space:
            regex = '^[a-zA-Z0-9]+$'
        if re.match(regex, data) is None:
            return False
        return True

    def is_string(self, data):
        if re.match('^[a-zA-Z]+$', data) is None:
            return False
        return True

    def is_number(self, data):
        if re.match('^[1-9]+[0-9]*$', str(data)) is None:
            return False
        return True

    def is_boolean(self, data):
        if data is not True and data is not False:
            return False
        return True

    def encode(self, clear):
        enc = []
        for i in range(len(clear)):
            key_c = SECRET_KEY[i % len(SECRET_KEY)]
            enc_c = (ord(clear[i]) + ord(key_c)) % 256
            enc.append(enc_c)
        return base64.urlsafe_b64encode(bytes(enc)).decode('utf-8')

    def decode(self, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = SECRET_KEY[i % len(SECRET_KEY)]
            dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    def md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def is_valid_json(self, data):
        try:
            json.loads(data)
            return True
        except:
            return False

    def client_error_response(self, message):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = message
        return Response(response, status=HTTP_400_BAD_REQUEST)

    def client_error_response_by_serializer(self, message):
        new_response = ''
        for key, val in message.items():
            new_response = "%s, %s" % (key, val[0])
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = new_response
        return Response(response, status=HTTP_400_BAD_REQUEST)

    def success_response(self, data):
        response = dict()
        response['status'] = SUCCESS_STATUS_CODE
        response['result'] = data
        return Response(response, status=HTTP_200_OK)

    def error_response(self):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = INTERNAL_SERVER_ERROR_CLIENT_MESSAGE
        return Response(response, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def no_data_found_response(self):
        response = dict()
        response['status'] = SUCCESS_STATUS_CODE
        response['result'] = 'No Data Found'
        return Response(response, status=HTTP_200_OK)

    def params_missing_response(self):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = 'Required params missing/incorrect(Bad request)'
        return Response(response, status=HTTP_400_BAD_REQUEST)

    def blocked_response(self):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = BLOCKED_CLIENT_MESSAGE
        return Response(response, status=HTTP_401_UNAUTHORIZED)

    def unauthorized_response(self):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = 'The request requires authentication. '
        return Response(response, status=HTTP_401_UNAUTHORIZED)

    def method_not_allowed_response(self):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = 'Method Not Allowed'
        return Response(response, status=HTTP_405_METHOD_NOT_ALLOWED)

    def not_acceptable_response(self):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = 'Request Not Acceptable'
        return Response(response, status=HTTP_406_NOT_ACCEPTABLE)

    def custom_error_response(self, status_code, message):
        response = dict()
        response['status'] = ERROR_STATUS_CODE
        response['result'] = message
        return Response(response, status=status_code)
