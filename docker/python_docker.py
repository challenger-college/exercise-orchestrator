from subprocess import run
from time import time

from test_injectors.python_injector import TestInjector, ChallengeInjector


class TestPythonDocker:

    def __init__(self, function_name, code, tests,
                 image="challenger_python_docker",
                 ):
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
        self.delete_file()
        self.execute_tests()


    def run_container(self, image):
        container = run(["docker", "run", "-d", image],
                        capture_output=True)
        if container.returncode == 0:
            self.id = self.decode_stdout(container.stdout)
            self.submit_file = f"{self.id}.py"
        else:
            raise Exception(f"Error while running container : {self.decode_stdout(container.stderr)}")

    def generate_file(self):
        with open(self.submit_file, "w") as file:
            file.write(self.code)
        self.success_code = TestInjector(self.function_name, self.tests,
                                         self.submit_file).add_tests()

    def delete_file(self):
        delete_command = run(["rm", self.submit_file], capture_output=True)

    def copy_file_in_container(self):
        copy = run(["docker", "cp", self.submit_file, f"{self.id}:/app"],
                   capture_output=True)
        if copy.returncode != 0:
            raise Exception(f"Error while copy of the file : {self.decode_stdout(copy.stderr)}")

    def execute_tests(self):
        start = time()
        command = ["docker", "exec", self.id, "python", self.submit_file]
        run_command = run(command, capture_output=True)
        if run_command.returncode == 0 and self.get_last_print(
                run_command.stdout) == self.success_code:
            self.status_code = 0
            self.output = f"Sucess"
            self.exec_time = (time() - start) * 1000
            return f"Success {time() - start}ms"
        elif run_command.returncode == 1:
            self.status_code = 1
            self.output = self.decode_stdout(run_command.stderr)
            self.exec_time = (time() - start) * 1000
            return f"Error : {self.decode_stdout(run_command.stderr)}"
        else:
            self.status_code = 1
            self.output = f"Error : votre code ne nous permet pas d'executer nos tests."
            self.exec_time = (time() - start) * 1000
            return f"Error : votre code ne nous permet pas d'executer nos tests."

    def is_running(self):
        status = run(["docker", "inspect", self.id,
                      "--format={{.State.Status}}"],
                     capture_output=True)
        result = self.decode_stdout(status.stdout)
        return result == "running"

    def get_last_print(self, string):
        string = self.decode_stdout(string)
        index = len(string) - 1
        while string[index] != "\n" and index != -1:
            index -= 1
        return string[index + 1: len(string)]

    @staticmethod
    def decode_stdout(bytes):
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
        if result[0] == "E":
            self.status_code = 1
            return "Challenge is not valid."
        else:
            self.status_code = 0
            return "Challenge is valid."


    @staticmethod
    def get_format_parameters(parameters):
        if len(parameters) == 1:
            return str(parameters[0])
        return ", ".join(parameters)

