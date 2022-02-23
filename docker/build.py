import logging
import subprocess

from docker.utils import DockerException, has_valid_docker_installation
from utils import get_format_std

IMAGES = {
    "python": "challenger_python"
}


def load_requirements():
    """Load docker requirements."""
    if has_valid_docker_installation():
        if not has_docker_images():
            logging.info("Docker images not found, building...")
            build_docker_images()
            logging.info("Docker images build with successful.")


def has_docker_images():
    """
    Verify if all docker images in IMAGES dictionary was build.

    Returns:
        bool: True if all docker images was build, else False.
    """
    for language, image_name in IMAGES.items():
        command = subprocess.run(["docker", "images", "-q", image_name],
                                 capture_output=True)
        if command.returncode != 0 or len(get_format_std(command.stdout)) == 0:
            return False
    return True


def build_docker_images():
    """
    Build all docker images in IMAGES dictionary.

    Returns:
        true: if building images has been successfully completed.
    """
    for language, image_name in IMAGES.items():
        logging.info(f"Building {language} docker image...")
        build = subprocess.run(["docker", "build", ".", "-f",
                                f"./dockerfiles/{language}", "-t",
                                image_name],
                               capture_output=True)
        if build.returncode != 0:
            logging.critical("Impossible to build docker images.")
            logging.critical(get_format_std(build.stderr))
            raise DockerException(f"Impossible to build docker images :"
                                  f" {get_format_std(build.stderr)}")
    return True


if __name__ == "__main__":
    load_requirements()
