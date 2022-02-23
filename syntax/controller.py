import subprocess
from abc import ABC, abstractmethod

from utils import get_format_std


class SyntaxCheckerException(Exception):
    pass


class SyntaxChecker(ABC):
    @abstractmethod
    def has_valid_syntax(self):
        pass

    @abstractmethod
    def get_syntax_error(self):
        pass


class PythonSyntaxChecker(SyntaxChecker):

    def __init__(self, path_file: str):
        self.file = path_file
        self.error = None

    def has_valid_syntax(self) -> bool:
        """
        Verify is the Python file has a valid syntax without execute it.

        Returns:
            bool: True if syntax is correct, else False.
        """
        command = ["python3", "-m", "py_compile", self.file]
        try:
            process = subprocess.run(command, capture_output=True)
            if process.returncode != 0:
                self.error = get_format_std(process.stderr)
                return False
            return True
        except subprocess.TimeoutExpired:
            SyntaxCheckerException("Python compilation command timeout expired.")

    def get_syntax_error(self):
        """Get attribute error"""
        return self.error


if __name__ == "__main__":
    t = PythonSyntaxChecker("test.py")
