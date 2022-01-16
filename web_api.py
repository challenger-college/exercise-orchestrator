import requests
import pprint

class Challenge:

    def __init__(self, function_name, parameters, tests, id):
        self.id = id
        self.function_name = function_name
        self.parameters = parameters
        self.tests = tests

    def valid_challenge(self, validy):
        requests.post(f"http://localhost:8000/api/challenge/{self.id}/check", params={"token": "API_TEST", "template": self.get_template(), "isValid": validy})


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
        response = requests.get(self.endpoint, params={"token": "API_TEST"})
        if 200 <= response.status_code <= 220:
            self.data = response.json()
        elif 400 <= response.status_code <= 420:
            self.status = 1
            self.error = response.json().get("error")
        else:
            self.status = 1
            self.error = "Error with request."

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


if __name__ == "__main__":
    response = requests.get("http://localhost:8000/api/challenges", params={"token": "API_TEST"})
    response = response.json()
    test = ChallengeParser().get_challenges()
    print(test[0].id)

