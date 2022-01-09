from subprocess import run
from time import time

from injector import TestInjector

class PythonDocker:

    def __init__(self, function_name, tests, image="challenger_python_docker",
                 submit_file="submit.py"):
        self.id = None
        self.success_code = None
        self.submit_file = submit_file
        self.function_name = function_name
        self.tests = tests

        self.run_container(image)
        self.copy_file_in_container()

    def run_container(self, image):
        container = run(["docker", "run", "-d", image],
                        capture_output=True)
        if container.returncode == 0:
            self.id = self.decode_stdout(container.stdout)
        else:
            raise f"Error while running container : {container.stderr}"

    def copy_file_in_container(self):
        self.success_code = TestInjector(self.function_name, self.tests,
                                         self.submit_file).add_tests()
        copy = run(["docker", "cp", self.submit_file, f"{self.id}:/app"],
                   capture_output=True)
        if copy.returncode != 0:
            raise f"Error while copy of the file : {copy.stderr}"

    def execute_tests(self):
        start = time()
        command = ["docker", "exec", self.id, "python", self.submit_file]
        run_command = run(command, capture_output=True)
        if run_command.returncode == 0 and self.get_last_print(run_command.stdout) == self.success_code:
            return f"Success {time()-start}ms"
        elif run_command.returncode == 1:
            return f"Error : {self.decode_stdout(run_command.stderr)}"
        else:
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
        while string[index] != "\n":
            index -= 1
        return string[index+1: len(string)]

    @staticmethod
    def decode_stdout(bytes):
        return bytes.decode("UTF-8").strip("\n")




if __name__ == "__main__":
    my_test = [
        [["1", "2"], "3"],
        [["1", "1"], "2"],
        [["45", "4"], "46"]
    ]
    my_test2 = [
        [[[1, 2, 3, 4]], [1, 2, 3, 4]]
    ]
    test = PythonDocker("sum_two_number", my_test)
    print(test.execute_tests())

