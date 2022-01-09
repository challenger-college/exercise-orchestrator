from sys import argv
from subprocess import run
from submit import my_function

def sum_two_numbers(a, b):
    return a + b

def decode_stdout(bytes):
    return bytes.decode("UTF-8").strip("\n")

def get_last_print(string):
    index = len(string) - 1
    while string[index] != "\n":
        index -= 1
    return string[index: len(string)]

if __name__ == "__main__":
    a = run(["python3", "submit.py"], capture_output=True)
    print(a.returncode)
    test = decode_stdout(a.stdout)
    print(get_last_print(test))