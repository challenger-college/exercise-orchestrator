import os
from subprocess import run
from time import time

from test_injectors.python_injector import TestInjector, ChallengeInjector

CONTAINER_TIME_OUT = os.getenv("CONTAINER_TIME_OUT")


class TestPythonDocker:

    def __init__(self, function_name, code, tests,
                 image="challenger_python",
                 ):
        CONTAINER_TIME_OUT = os.getenv("CONTAINER_TIME_OUT")
        self.id = None
        self.success_code = None
        self.submit_file = None
        self.function_name = function_name
        self.tests = tests
        self.code = code
        self.status_code = 0
        self.output = None
        self.exec_time = None

        self.run_container(image)
        self.generate_file()
        self.copy_file_in_container()
        if self.is_valid_syntax():
            self.inject_tests()
            self.copy_file_in_container()
            self.execute_tests()
        self.delete_file()

    def run_container(self, image):
        CONTAINER_TIME_OUT = os.getenv("CONTAINER_TIME_OUT")
        container = run(["docker", "run", "-d", "--env", f"CONTAINER_TIME_OUT={CONTAINER_TIME_OUT}", image],
                        capture_output=True)
        if container.returncode == 0:
            self.id = self.decode_bytes(container.stdout)
            self.submit_file = f"{self.id}.py"
        else:
            raise Exception(
                f"Error while running container : {self.decode_bytes(container.stderr)}")

    def generate_file(self):
        with open(self.submit_file, "w") as file:
            file.write(self.code)

    def inject_tests(self):
        self.success_code = TestInjector(self.function_name, self.tests,
                                         self.submit_file).add_tests()

    def delete_file(self):
        delete_command = run(["rm", self.submit_file], capture_output=True)

    def copy_file_in_container(self):
        copy = run(["docker", "cp", self.submit_file, f"{self.id}:/main.py"],
                   capture_output=True)
        if copy.returncode != 0:
            raise Exception(
                f"Error while copy of the file : {self.decode_bytes(copy.stderr)}")

    def is_valid_syntax(self):
        run_file = run(["docker", "exec", self.id, "python", "main.py"],
                       capture_output=True)
        if run_file.returncode != 0:
            self.status_code = 1
            self.output = self.decode_bytes(run_file.stderr)
            return False
        return True

    def execute_tests(self):
        if not self.is_running():
            self.status_code = 1
            self.output = "Temps dépassé, votre script est trop lent..."
        command = ["docker", "exec", self.id, "python", "main.py"]
        run_command = run(command, capture_output=True)

        std_out = self.decode_bytes(run_command.stdout)
        std_err = self.decode_bytes(run_command.stderr)
        code_validity = self.random_code_is_valid(std_out)

        if run_command.returncode == 0 and code_validity:
            self.exec_time = float(self.get_line_from_end(std_out, 1))
            self.status_code = 0
            self.output = "Bravo, vous avez reussi le challenge !"
        elif run_command.returncode == 0 and not code_validity:
            self.output = "Erreur, votre code ne nous permet d'executer nos tests"
            self.status_code = 1
        elif run_command.returncode == 1 and code_validity:
            if self.get_line_from_end(std_err, 0) == "3":
                self.output = self.get_line_from_end(std_err, 1)
                self.status_code = 1
            else:
                self.output = std_err
                self.status_code = 1
        elif run_command.returncode == 1 and not code_validity:
            self.output = "Erreur, votre code ne nous permet d'executer nos tests"
            self.status_code = 1
        elif run_command.returncode == 137:
            self.status_code = 1
            self.output = "Temps dépassé, votre script est trop lent..."

    def is_running(self):
        status = run(["docker", "inspect", self.id,
                      "--format={{.State.Status}}"],
                     capture_output=True)
        result = self.decode_bytes(status.stdout)
        return result == "running"

    def random_code_is_valid(self, string):
        return self.get_line_from_end(string, 0) == str(self.success_code)

    @staticmethod
    def get_lines_except_lines_from_end(string, line_number):
        lines = string.splitlines()
        return lines[:-line_number]

    @staticmethod
    def get_line_from_end(string, line_number):
        lines = string.splitlines()
        if len(lines) == 0 or line_number >= len(lines):
            return ""
        else:
            lines.reverse()
            return lines[line_number]

    @staticmethod
    def decode_bytes(bytes):
        return bytes.decode("UTF-8").strip("\n")


class ChallengePythonDocker(TestPythonDocker):

    def __init__(self, function_name, tests, parameters):
        self.function_name = function_name
        self.tests = tests
        self.parameters = parameters
        self.generate_basic_code()
        super().__init__(self.function_name, self.code, self.tests)

    def generate_basic_code(self):
        self.code = f"def {self.function_name}({self.get_format_parameters(self.parameters)}):\n    pass"

    def generate_file(self):
        with open(self.submit_file, "w") as file:
            file.write(self.code)
        self.success_code = ChallengeInjector(self.function_name, self.tests,
                                              self.submit_file).add_tests()

    def execute_tests(self):
        result = super().execute_tests()
        self.status_code = 0
        return
        # if result[0] == "E":
        #     self.status_code = 1
        #     return "Challenge is not valid."
        # else:
        #     self.status_code = 0
        #     return "Challenge is valid."

    @staticmethod
    def get_format_parameters(parameters):
        if len(parameters) == 1:
            return str(parameters[0])
        return ", ".join(parameters)
