from abc import ABC
from rest_framework import authentication
from .settings import VERSION
from utils.general_methods import GeneralMethods


class Middleware(authentication.BaseAuthentication, ABC):

    def __init__(self, get_response):
        self.get_response = get_response
        self.gm = GeneralMethods()

    def __call__(self, request, *args, **kwargs):
        path = request.get_full_path()

        """
            Making sure middleware to run before View
            Write code here, will run before view.py
        """
        ##

        """
            self.get_response(request),
            Responsible to continue the execution of view.py
        """
        response = self.get_response(request)

        """
            Write code here, will run after view.py
        """

        # Write code here

        """
            To send version in response
        """

        response['version'] = VERSION
        return response
