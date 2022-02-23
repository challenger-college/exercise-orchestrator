from syntax.controller import PythonSyntaxChecker

r = PythonSyntaxChecker("test.py")
if not r.has_valid_syntax():
    print(r.get_syntax_error())