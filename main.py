from time import sleep
from dotenv import load_dotenv
import os

from docker.python_docker import ChallengePythonDocker, TestPythonDocker
from web_api.exercise import ExerciseParser
from web_api.challenge import ChallengeParser


def main():
    while True:
        verify_challenges()
        verify_exercises()
        sleep(0.5)


def verify_challenges():
    challenges = ChallengeParser().get_challenges()
    for challenge in challenges:
        current_challenge = ChallengePythonDocker(challenge.function_name,
                                                  challenge.tests,
                                                  challenge.parameters)
        if current_challenge.status_code == 0:
            print(f"Je valide le challenge {current_challenge.function_name}")
            challenge.valid_challenge("true")
        else:
            print(f"Je refuse le challenge {current_challenge.function_name}")
            challenge.valid_challenge("false")


def verify_exercises():
    exercises = ExerciseParser().get_exercise()
    for exercise in exercises:
        current_exercise = TestPythonDocker(exercise.function_name,
                                            exercise.code, exercise.tests)
        if current_exercise.status_code == 0:
            print(f"Je valide l'exercice {current_exercise.function_name} exec time {current_exercise.exec_time}")
            exercise.valid_exercise("true", current_exercise.output, current_exercise.exec_time)
        else:
            print(f"Je refuse l'exercice {current_exercise.function_name} exec time {current_exercise.exec_time}")
            exercise.valid_exercise("false", current_exercise.output, current_exercise.exec_time)


if __name__ == "__main__":
    main()
