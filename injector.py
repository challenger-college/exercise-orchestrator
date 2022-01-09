from random import randint


class TestInjector:

    def __init__(self, function_name, tests, file="submit.py"):
        self.success_code = str(randint(0, 10**9))
        self.tests = tests
        self.file = file
        self.function_name = function_name

    def write(self, lines):
        with open(self.file, "a") as file:
            for line in lines:
                file.write(f"\n{line}")

    def add_sys_import(self):
        self.write(["import sys"])

    def add_tests(self):
        self.add_sys_import()
        for test in self.tests:
            code = ["",
                    f"result = {self.function_name}({self.get_format_args(test[0])})",
                    f"if result != {test[1]}:",
                    f"    print('la réponse de {self.function_name}({self.get_format_args(test[0])}) est {test[1]}, cependant votre résultat est ' + str(result), file=sys.stderr)",
                    f"    exit(1)"]
            self.write(code)
        end = [f"print({self.success_code})", "exit(0)"]
        self.write(end)
        return self.success_code

    @staticmethod
    def get_format_args(args):
        if len(args) == 1:
            return str(args[0])
        return ", ".join(args)

if __name__ == "__main__":
    my_test = [
        [["1", "2"], "3"],
        [["1", "1"], "2"],
        [["45", "1"], "46"]
    ]
    t = TestInjector("my_function", my_test)
