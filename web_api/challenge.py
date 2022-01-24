import os

from web_api.requests_api import RequestVerification

import var_env
IP = os.getenv("IP_WEBSERVICE")
TOKEN = os.getenv("API_TOKEN")


class Challenge:

    def __init__(self, function_name, parameters, tests, id, timeout=1000):
        self.id = id
        self.timeout = timeout
        self.function_name = function_name
        self.parameters = parameters
        self.tests = tests

    def valid_challenge(self, validity):
        params = {"token": "API_TEST", "template": self.get_template(),
                  "isValid": validity}
        request = RequestVerification.post_request(
            f"http://{IP}/api/challenge/{self.id}/check",
            params=params)
        if request == 0:
            return
        context = f"send challenge status to API  ({self.id})"
        if RequestVerification.verify(request, context):
            return

    def get_template(self):
        code = f"def {self.function_name}({self.get_format_args(self.parameters)}):\n    "
        return code

    @staticmethod
    def get_format_args(args):
        if len(args) == 1:
            return str(args[0])
        return ", ".join(args)


class ChallengeParser:

    def __init__(self, ip="localhost:8000"):
        self.endpoint = f"http://{ip}/api/challenges"
        self.data = None
        self.status = 0
        self.error = None

    def is_valid_status(self):
        return self.status == 0

    def send_request(self):
        request = RequestVerification.get_request(self.endpoint,
                                                  params={"token": "API_TEST"})
        if request == 0:
            return
        context = f"get all challenges not validated"
        if RequestVerification.verify(request, context):
            self.data = request.json()

    def get_challenges(self):
        self.send_request()
        if self.data:
            challenges = []
            for challenge in self.data:
                id = challenge.get("id")
                function_name = challenge.get("function_name")
                tests = self.get_tests(challenge.get("tests"))
                parameters = self.get_parameters(challenge.get("tests"))
                challenges.append(
                    Challenge(function_name, parameters, tests, id))
            return challenges
        return []

    @staticmethod
    def get_tests(tests):

        format_tests = []
        for test in tests:
            format_test = [[]]
            for input in test.get("inputs"):
                format_test[0].append(input.get("value"))
            format_test.append(test.get("output"))
            format_tests.append(format_test)
        return format_tests

    @staticmethod
    def get_parameters(tests):
        parameters = []
        for parameter in tests[0].get("inputs"):
            parameters.append(parameter.get("name"))
        return parameters
