import subprocess
from subprocess import run
from time import time


class PythonDocker:

    def __init__(self, image="challenger_python_docker"):
        self.id = None
        self.submit_file = "submit.py"

        self.run_container(image)
        self.copy_file_in_container(self.submit_file)

    def run_container(self, image):
        container = run(["docker", "run", "-d", image],
                        capture_output=True)
        if container.returncode == 0:
            self.id = self.decode_stdout(container.stdout)
        else:
            raise f"Error while running container : {container.stderr}"

    def copy_file_in_container(self, file):
        copy = run(["docker", "cp", file, f"{self.id}:/app"],
                   capture_output=True)
        if copy.returncode != 0:
            raise f"Error while copy of the file : {copy.stderr}"

    def execute_test(self, args):
        command = ["docker", "exec", self.id, "python", self.submit_file]
        for arg in args:
            command.append(str(arg))
        command_test = run(command, capture_output=True)
        if command_test.returncode == 0:
            return {"status_code": 0,
                    "result": self.decode_stdout(command_test.stdout)}
        else:
            return {"status_code": 1,
                    "result": self.decode_stdout(command_test.stderr)}

    def execute_tests(self, tests):
        start = time()
        for test in tests:
            result = self.execute_test(test[0])
            if result.get("status_code") == 1 and not self.is_running():
                return "Time limit exceeded"
            elif result.get("status_code") == 1:
                return result.get("result")
            else:
                if str(test[1]) != result.get("result"):
                    return f"Ereur, votre resultat est {result.get('result')} alors que {test[1]} est attendu"
        return f"Success {time()-start}ms"

    def is_running(self):
        status = run(["docker", "inspect", self.id,
                      "--format={{.State.Status}}"],
                     capture_output=True)
        result = self.decode_stdout(status.stdout)
        return result == "running"

    @staticmethod
    def decode_stdout(bytes):
        return bytes.decode("UTF-8").strip("\n")


if __name__ == "__main__":
    my_test = [
        [[1, 2], 3],
        [[1, 1], 2],
        [[45, 1], 46]
    ]
    test = PythonDocker()
    print(test.execute_tests(my_test))

