import sys
import requests

class RequestVerification:

    @staticmethod
    def verify(request, context):
        if request.ok:
            return 1
        elif 400 <= request.status_code < 500:
            try:
                print(f"Error during : {context} : {request.json()} ", file=sys.stderr)
            except:
                print(f"Error during : {context}", file=sys.stderr)
        else:
            print(f"Error during : {context}", file=sys.stderr)

    @staticmethod
    def post_request(url, params={}):
        try:
            request = requests.post(url=url, params=params)
            return request
        except:
            print(
                "Error during connection with web api, please verify his status",
                file=sys.stderr)
            return 0

    @staticmethod
    def get_request(url, params={}):
        try:
            request = requests.get(url=url, params=params)
            return request
        except:
            print(
                "Error during connection with web api, please verify his status",
                file=sys.stderr)
            return 0