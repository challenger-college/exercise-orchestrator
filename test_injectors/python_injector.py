from random import randint
class I:
    def __init__(S,f,T,f):S.s=str(randint(0,10**9));S.t=T;S.f=f;S.f=f
    def write(S,L):
        with open(S.f,"a") as F:
            for l in L:F.write(f"\n{l}")
    def add_sys_import(S):S.write(["import sys"])
    def add_tests(S):
        S.add_sys_import()
        for test in S.t:
            c=["",f"result = {S.function_name}({S.get_format_args(test[0])})",f"if result != {test[1]}:",f"    print('la réponse de {S.function_name}({S.get_format_args(test[0])}) est {test[1]}, cependant votre résultat est ' + str(result), file=sys.stderr)",f"    exit(1)"]
            S.write(c)
        S.write([f"print({S.success_code})", "exit(0)"]);return S.s
    @staticmethod
    def get_format_args(a):
        if len(a) == 1:
            return str(a[0])
        return ", ".join(a)
class ChallengeInjector(I):
    def __init__(S, f, t, F):
        super().__init__(f, t, F)
    def add_tests(S):
        S.add_sys_import()
        for test in S.t:c=["",f"result = {S.function_name}({S.get_format_args(test[0])})",f"if result != {test[1]}:",f"    pass"];S.write(c)
        S.write([f"print({S.success_code})","exit(0)"]);return S.s
