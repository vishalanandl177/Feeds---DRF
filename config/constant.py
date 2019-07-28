# Do not change the variable name

UNAUTHORIZED = 'Unauthorized'
SESSION_EXPIRED = 'Session Expired'
NOT_ACCEPTABLE = 'Not Acceptable'
BAD_REQUEST = 'Bad Request'
FORBIDDEN = 'Forbidden'
INTERNAL_SERVER_ERROR = 'Internal Server Error'
INTERNAL_SERVER_ERROR_CLIENT_MESSAGE = \
    'The server encountered an unexpected condition which prevented it from fulfilling the request.'
INSUFFICIENT_PARAM = 'Required params missing or incorrect'
INSUFFICIENT_HEADERS = 'Required headers missing or incorrect'
BLOCKED_CLIENT_MESSAGE = 'The network administrator has prevented you from using the network'
NO_USER_FOUND = 'No User Found'

"""
    The code to sent as a part of response to web users and app users.
    If error occurs, ERROR_STATUS_CODE is responsible for identification of error status code.
    If success, SUCCESS_STATUS_CODE is responsible for identification of success status code.
"""
ERROR_STATUS_CODE = False
SUCCESS_STATUS_CODE = True
