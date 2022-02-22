import subprocess

from docker.utils import get_format_std, DockerException


class ContainerDocker:
    """
    Class to instance containers and manage it.

    Args:
        image (str): Name or id of the docker image.
        env (dict): Dictionary with environment variables loaded in the
            container.
        command_timeout (int): Timeout when executing docker commands.
    """

    def __init__(self, image: str, env: dict = None, command_timeout: int = 10):

        self.image = image
        self.env = env
        self.id = None
        self.command_timeout = command_timeout

    def run(self, options: dict = None) -> str:
        """
        Run a docker container with variables environment and options.

        Args:
            options (dict): Set options in dictionary with flags in key
                and arguments in value. Defaults to None.

        Returns:
            str: Container id.

        Raises:
            DockerException: If an error is encountered during the running of
                the container.
        """
        if self.is_running():
            raise DockerException("Container is already running.")
        process_command = ["docker", "run", "-d"]
        if self.env is not None and isinstance(self.env, dict):
            if len(self.env) > 0:
                process_command.append("--env")
            for key, value in self.env.items():
                process_command.append(f"{key}={value}")
        if options is not  None and isinstance(options, dict):
            if len(options) > 0:
                for key, value in options.items():
                    process_command.append(key)
                    process_command.append(value)
        process_command.append(self.image)
        try:
            process = subprocess.run(process_command, capture_output=True,
                                     timeout=self.command_timeout)
            if process.returncode != 0:
                raise DockerException(get_format_std(process.stderr))
            else:
                self.id = get_format_std(process.stdout)
                return self.id
        except subprocess.TimeoutExpired:
            raise DockerException("Command time out expired.")

    def kill(self) -> bool:
        """
        Kill the current running container.

        Returns:
            true: If the container has been killed with successful.

        Raises:
            DockerException: If an error is encountered during the kill process of
                the container.

        """
        if not self.is_running():
            raise DockerException("Container is not running.")
        else:
            process_command = ["docker", "kill", self.id]
            try:
                process = subprocess.run(process_command, capture_output=True,
                                         timeout=self.command_timeout)
                if process.returncode != 0:
                    raise DockerException(get_format_std(process.stderr))
                return True
            except subprocess.TimeoutExpired:
                raise DockerException("Command time out expired.")

    def is_running(self) -> bool:
        """
        Get status of the container.

        Returns:
            bool: True if the container is currently running, else False.

        Raises:
            DockerException: If an error is encountered during the state
                verification of the container.
        """
        if self.id is None:
            return False
        else:
            process_command = ["docker", "inspect",
                               "--format={{.State.Status}}",
                               self.id]
            try:
                process = subprocess.run(process_command, capture_output=True,
                                         timeout=self.command_timeout)
                if process.returncode != 0:
                    raise DockerException(get_format_std(process.stderr))
                else:
                    return get_format_std(process.stdout) == "running"
            except subprocess.TimeoutExpired:
                raise DockerException("Command time out expired.")

    def exec_command(self, command: list) -> dict:
        """
        Execute a command in the container.

        Args:
            command (list): Argument of the command separated in a list.

        Returns:
            dict: Dictionary with the result of the command "returncode",
                "stderr" and "stdout".

        Raises:
            DockerException: If the container is not running.
        """
        if not self.is_running():
            raise DockerException("Container is not running.")
        process_command = ["docker", "exec", self.id]
        for arg in command:
            process_command.append(arg)
        process = subprocess.run(process_command, capture_output=True)
        command_state = {
            "returncode": process.returncode,
            "stderr": get_format_std(process.stderr),
            "stdout": get_format_std(process.stdout)
        }
        return command_state

    def copy_file(self, src_path: str, dest_path: str = "/"):
        """
        Copy a file in the container.

        Args:
            src_path (str): Path of the source file.
            dest_path (str): Path of the destination file. Defaults to "/"
                (container root directory).

        Returns:
            true: If the file has been copy with successful in the container.

        Raises:
            DockerException: If an error is encountered during the file copy
                in the container.
        """
        if not self.is_running():
            raise DockerException("Container is not running.")
        process_command = ["docker", "cp", src_path, f"{self.id}:{dest_path}"]
        try:
            process = subprocess.run(process_command, capture_output=True,
                                     timeout=self.command_timeout)
            if process.returncode != 0:
                raise DockerException(get_format_std(process.stderr))
            return True
        except subprocess.TimeoutExpired:
            raise DockerException("Command time out expired.")

