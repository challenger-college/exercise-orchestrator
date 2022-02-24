from time import sleep;from dotenv import load_dotenv;import os;from docker.python_docker import ChallengePythonDocker,TestPythonDocker;from web_api.exercise import ExerciseParser;from web_api.challenge import ChallengeParser
def main():
    while True:
        verify_challenges()
        verify_exercises()
        sleep(0.5)
def verify_challenges():
    c=ChallengeParser().get_challenges()
    for C in c:
        a=ChallengePythonDocker(C.function_name,C.tests,C.parameters)
        if a.status_code==0:
            print(f"Je valide le challenge {a.function_name}")
            C.valid_challenge("true")
        else:
            print(f"Je refuse le challenge {a.function_name}")
            C.valid_challenge("false")
def verify_exercises():
    e = ExerciseParser().get_exercise()
    for E in e:
        c=TestPythonDocker(E.function_name,E.code,E.tests)
        if c.status_code==0:
            print(f"Je valide l'exercice {c.function_name} exec time {c.exec_time}")
            E.valid_exercise("true",c.output,c.exec_time)
        else:
            print(f"Je refuse l'exercice {c.function_name} exec time {c.exec_time}")
            E.valid_exercise("false",c.output,c.exec_time)
if __name__ == "__main__":main()
