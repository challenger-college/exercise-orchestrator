import logging
from subprocess import run

IMAGES = {
    "python": "challenger_python"
}


class DockerRequirements:

    def load(self):
        self.has_valid_docker_installation()
        if not self.has_docker_images():
            logging.info("Docker images not found, building...")
            self.build_docker_images()
            logging.info("Docker images build with successful.")

    @staticmethod
    def has_valid_docker_installation():
        docker_version = run(["docker", "--version"], capture_output=True)
        if docker_version.returncode != 0:
            logging.critical("Please install docker, it's a requirement.")
            exit(1)
        return True

    @staticmethod
    def build_docker_images():
        for language, image_name in IMAGES.items():
            logging.info(f"Building {language} docker image...")
            build = run(["docker", "build", ".", "-f",
                         f"./docker/dockerfiles/{language}", "-t", image_name],
                        capture_output=True)
            if build.returncode != 0:
                logging.critical("Impossible to build docker images.")
                logging.critical(build.stderr.decode("UTF-8"))
                exit(1)
        return True

    @staticmethod
    def has_docker_images():
        for language, image_name in IMAGES.items():
            command = run(["docker", "images", "-q", image_name],
                          capture_output=True)
            if command.returncode != 0 or len(
                    command.stdout.decode("UTF-8")) == 0:
                return False
        return True
