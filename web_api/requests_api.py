import requests
import logging


class RequestVerification:

    @staticmethod
    def verify(request, context):
        if request.ok:
            return True
        else:
            try:
                logging.error(
                    f"Unable to connect to the Web API [{request.status_code}]: {context} {request.json()}.")
            except:
                logging.error(f"Unable to connect to the Web API [{request.status_code}]: {context}.")

    @staticmethod
    def post_request(url, params={}):
        try:
            request = requests.post(url=url, params=params)
            return request
        except:
            logging.error(
                "Unable to connect to the Web API, please check its status.")
            return 0

    @staticmethod
    def get_request(url, params={}):
        try:
            request = requests.get(url=url, params=params)
            return request
        except:
            logging.error(
                "Unable to connect to the Web API, please check its status.")
        return 0
