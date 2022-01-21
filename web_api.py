import requests
import pprint

class RequestVerification:

    @staticmethod
    def verify(request):
        if request.ok:
            return 1
        elif 400 <= request.status_code < 500:
            raise Exception(f"Error with code : {request.status_code}")
        else:
            raise Exception("Error with the request")


class Challenge:

    def __init__(self, function_name, parameters, tests, id, timeout=1000):
        self.id = id
        self.timeout = timeout
        self.function_name = function_name
        self.parameters = parameters
        self.tests = tests

    def valid_challenge(self, validy):
        params = {"token": "API_TEST", "template": self.get_template(), "isValid": validy}
        request = requests.post(f"http://localhost:8000/api/challenge/{self.id}/check",
                                params=params)
        if RequestVerification.verify(request):
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
        request = requests.get(self.endpoint, params={"token": "API_TEST"})
        if RequestVerification.verify(request):
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
                challenges.append(Challenge(function_name, parameters, tests, id))
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


class Exercise:
    def __init__(self, code, function_name, tests, exercise_id, timeout):
        self.id = exercise_id
        self.function_name = function_name
        self.tests = tests
        self.code = code
        self.timeout = timeout

    def valid_challenge(self, validy, error=None):
        request = requests.post(f"http://localhost:8000/api/exercice/{self.id}/check", params={"token": "API_TEST", "isValid": validy, "error": error})
        if RequestVerification.verify(request):
            return


class ExerciseParser:

    def __init__(self, ip="localhost:8000"):
        self.endpoint = f"http://{ip}/api/exercices"
        self.data = None
        self.status = 0
        self.error = None

    def is_valid_status(self):
        return self.status == 0

    def send_request(self):
        request = requests.get(self.endpoint, params={"token": "API_TEST"})
        if RequestVerification.verify(request):
            self.data = request.json()

    def get_exercise(self):
        self.send_request()
        if self.data:
            exercises = []
            for exercise in self.data:
                id = exercise.get("id")
                function_name = exercise.get("challenge").get("function_name")
                timeout = exercise.get("challenge").get("timeout")
                code = exercise.get("content")
                tests = self.get_tests(exercise.get("challenge").get("tests"))
                exercises.append(Exercise(code, function_name, tests, id, timeout))
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

if __name__ == "__main__":
    response = requests.get("http://localhost:8000/api/challenges", params={"token": "API_TEST"})
    response = response.json()
    test = ChallengeParser().get_challenges()
    print(test[0].id)

