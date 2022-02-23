import logging
import subprocess


class DockerException(Exception):
    pass


def has_valid_docker_installation():
    """
    Verify if docker is install.

    Returns:
        bool: True if docker is install, else False.
    """
    docker_version = subprocess.run(["docker", "--version"],
                                    capture_output=True)
    if docker_version.returncode != 0:
        logging.critical("Please install docker, it's a requirement.")
        return False
    return True
