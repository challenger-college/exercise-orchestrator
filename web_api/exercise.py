import os

from web_api.requests_api import RequestVerification
from variables_env import load_environment_variable, get_token_api, get_web_service_ip

load_environment_variable()
IP = get_web_service_ip()
TOKEN = get_token_api()


class Exercise:

    def __init__(self, code, function_name, tests, exercise_id, timeout, token):
        self.id = exercise_id
        self.function_name = function_name
        self.tests = tests
        self.code = code
        self.timeout = timeout
        self.token = token

    def valid_exercise(self, validity, error=None, time=None):
        request = RequestVerification.post_request(
            f"http://{IP}/api/exercise/{self.id}/check/{self.token}",
            params={"token": "API_TEST", "isValid": validity, "output": error,
                    "time": time})
        if request == 0:
            return
        context = f"send exercise status to API  ({self.id})"
        if RequestVerification.verify(request, context):
            return


class ExerciseParser:

    def __init__(self):
        self.endpoint = f"http://{IP}/api/exercises"
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
        context = "Get all exercises submit"
        if RequestVerification.verify(request, context):
            self.data = request.json()

    def get_exercise(self):
        self.send_request()
        if self.data:
            exercises = []
            for exercise in self.data:
                id = exercise.get("id")
                token = exercise.get("token")
                function_name = exercise.get("challenge").get("function_name")
                timeout = exercise.get("challenge").get("timeout")
                code = exercise.get("content")
                tests = self.get_tests(exercise.get("challenge").get("tests"))
                exercises.append(
                    Exercise(code, function_name, tests, id, timeout, token))
            return exercises
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
