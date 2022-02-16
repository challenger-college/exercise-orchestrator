from time import sleep
import os
import logging

from variables_env import load_environment_variable, get_web_service_ip
from docker.python_docker import ChallengePythonDocker, TestPythonDocker
from web_api.exercise import ExerciseParser
from web_api.challenge import ChallengeParser
from logs import load_logs
from docker.docker_requirements import DockerRequirements


def main():
    load_logs()
    load_environment_variable()
    DockerRequirements().load()
    logging.info(f"Orchestrator started (WebService IP : {get_web_service_ip()})")
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
            logging.info(f"The challenge ({current_challenge.function_name}) has been validated [ID {current_challenge.id}].")
            challenge.valid_challenge("true")
        else:
            logging.info(f"The challenge ({current_challenge.function_name}) has been rejected [ID {current_challenge.id}].")
            challenge.valid_challenge("false")


def verify_exercises():
    exercises = ExerciseParser().get_exercise()
    for exercise in exercises:
        current_exercise = TestPythonDocker(exercise.function_name,
                                            exercise.code, exercise.tests)
        if current_exercise.status_code == 0:
            logging.info(f"The exercise ({current_exercise.function_name}) has been validated in {current_exercise.exec_time}ms [ID {current_exercise.id}].")
            exercise.valid_exercise("true", current_exercise.output, current_exercise.exec_time)
        else:
            logging.info(f"The exercise ({current_exercise.function_name}) has been rejected [ID {current_exercise.id}].")
            exercise.valid_exercise("false", current_exercise.output, current_exercise.exec_time)


if __name__ == "__main__":
    main()
