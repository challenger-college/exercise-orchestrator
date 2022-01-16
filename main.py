import time

from web_api import *
from python_docker import ChallengePythonDocker
from time import sleep

def main():
    while True:
        challenges = ChallengeParser().get_challenges()
        for challenge in challenges:
            current_challenge = ChallengePythonDocker(challenge.function_name, challenge.tests, challenge.parameters)
            if current_challenge.status_code == 0:
                print(f"Je valide le challenge {current_challenge.function_name}")
                challenge.valid_challenge("true")
            else:
                print(f"Je refuse le challenge {current_challenge.function_name}")
                challenge.valid_challenge("false")
        time.sleep(1)




if __name__ == "__main__":
    main()