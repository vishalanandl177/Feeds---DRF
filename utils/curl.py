import requests

"""
    Class:              Curl
    Description:        For server-side API call
"""


class Curl:
    """
        Function:       __init__
        Input:          headers: Dictionary (Optional)
    """
    headers = dict()

    def __init__(self, headers=None):
        if headers:
            self.headers.update(headers)

    """
        Function:       get  
        Input:          api: String (required), params: Dict (Optional), headers: Dictionary (Optional)
        Output:         response: JSON, status_code, headers
    """

    def get(self, api, params=None, headers=None, cookies=None, auth=None, timeout=None):
        if not api:
            return False
        if headers:
            self.headers.update(headers)
        response = requests.get(api, params,
                                headers=self.headers, cookies=cookies, auth=auth, timeout=timeout)
        return response.json(), response.status_code, response.request.headers

    """
        Function:       post  
        Input:          api: String (required), params: Dict (Optional), headers: Dictionary (Optional)
        Output:         response: JSON, status_code, headers
    """

    def post(self, api, params=None, headers=None, cookies=None, auth=None, timeout=None):
        if not api:
            return False
        if headers:
            self.headers.update(headers)
        response = requests.post(api, params, headers=self.headers,
                                 cookies=cookies, auth=auth, timeout=timeout)
        return response.json(), response.status_code, response.request.headers

    """
       Function:       update_headers  
       Input:          headers: Dict (Optional)
       Output:         response: headers
   """

    def update_headers(self, headers=None):
        if headers:
            self.headers.update(headers)
            return self.headers
        else:
            return self.headers
