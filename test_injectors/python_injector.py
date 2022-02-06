from random import randint


class TestInjector:

    def __init__(self, function_name, tests, file):
        self.success_code = str(randint(0, 10**9))
        self.tests = tests
        self.file = file
        self.function_name = function_name
        self.template = """
import sys, time


class TestsFactory:

    def __init__(self, function, function_name, tests, secret_code, timeout=4000):
        self.function = function
        self.function_name = function_name
        self.tests = tests
        self.secret_code = secret_code
        self.execute_tests()

    def assert_is_equal(self, test, response):
        fail = False
        try:
            result = self.function(*test)
            if result != response:
                if isinstance(result, (str)):
                    print(f'Réponse incorrecte avec {self.function_name}({self.get_format_args(test)}), votre résultat est "{result}" alors que la réponse attentue est {response}',
                          file=sys.stderr)
                else:
                    print(f'Réponse incorrecte avec {self.function_name}({self.get_format_args(test)}), votre résultat est {result} alors que la réponse attentue est {response}',
                          file=sys.stderr)
                print(3, file=sys.stderr)
                fail = True
        except:
            if not fail:
                error_result = self.get_last_error()

                print(f"Line {error_result.get('line')}", file=sys.stderr)
                print(error_result.get("error"), file=sys.stderr)
                fail = True
        if fail:
            print(self.secret_code)
            exit(1)

    def execute_tests(self):
        start = time.time()
        for test in self.tests:
            self.assert_is_equal(test[0], test[1])
        exec_time = round((time.time() - start) * 1000, 3)
        print(f"{exec_time}")
        print(self.secret_code)

    @staticmethod
    def get_last_error():
        error = sys.exc_info()
        error_data = {"error": error[1]}
        if error[2] is not None:
            error = error[2]
        else:
            return error_data
        while error.tb_next is not None:
            error = error.tb_next
        error_data.update({"line": error.tb_lineno})
        return error_data

    @staticmethod
    def get_format_args(args):
        if len(args) == 1:
            return str(args[0])
        args = [str(arg) for arg in args]
        return ", ".join(args)


if __name__ == "__main__":
        """

    def write(self, lines):
        with open(self.file, "a") as file:
            for line in lines:
                file.write(f"\n{line}")

    def add_tests(self):
        code = ["",
                self.template,
                f"    tests = {self.reformat_tests(self.tests)}",
                f"    factory = TestsFactory({self.function_name}, '{self.function_name}', tests, {self.success_code})",
                ]
        self.write(code)
        return self.success_code

    def get_format_parameters(self, parameters):
        if len(parameters) == 1:
            return str(parameters[0])
        return ", ".join(parameters)

    def reformat_tests(self, tests):
        string = []
        for test in tests:
            string.append(f"[[{self.get_format_parameters(test[0])}], {test[1]}]")
        return "[" + ", ".join(string) + "]"

    @staticmethod
    def get_format_args(args):
        if len(args) == 1:
            return str(args[0])
        return ", ".join(args)


class ChallengeInjector(TestInjector):

    def __init__(self, function_name, tests, file):
        super().__init__(function_name, tests, file)

    def add_tests(self):
        for test in self.tests:
            code = ["",
                    f"result = {self.function_name}({self.get_format_args(test[0])})",
                    f"if result != {test[1]}:",
                    f"    pass",
                    ]
            self.write(code)
        end = [f"print({self.success_code})", "exit(0)"]
        self.write(end)
        return self.success_code
