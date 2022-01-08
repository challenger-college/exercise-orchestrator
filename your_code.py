from sys import argv
from subprocess import run

def sum_two_numbers(a, b):
    return a + b


if __name__ == "__main__":
    a = run(["echo", "sexed"], capture_output=True)
    print(a.stdout.decode("UTF-8").strip("\n"))