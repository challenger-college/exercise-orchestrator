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


def get_format_std(stream: bytes) -> str:
    """
    Format stderr or stdout stream into a string with trailing whitespace
    removed.

    Args:
        stream (bytes): Stdout or stderr stream.

    Returns:
        str: Format string with trailing whitespace.
    """
    return stream.decode("utf-8").rstrip()
