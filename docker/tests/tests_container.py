from unittest import TestCase, mock

from docker.container import ContainerDocker, DockerException


class TestDockerContainer(TestCase):

    def test_create_object(self):
        container = ContainerDocker("challenger_python")
        self.assertIsInstance(container, ContainerDocker)

    def test_run_container_with_invalid_image(self):
        container = ContainerDocker("random_image123")
        self.assertRaises(DockerException, container.run)

    def test_run_container_with_valid_env(self):
        env = {"TEST": 147}
        container = ContainerDocker("challenger_python", env=env)
        self.assertIsInstance(container.run(), str)

    def test_run_container_with_invalid_env(self):
        env = [1, 2, 3]
        container = ContainerDocker("challenger_python", env=env)
        self.assertIsInstance(container.run(), str)

    def test_run_container_with_options(self):
        container = ContainerDocker("challenger_python")
        self.assertIsInstance(container.run({"--network": "none"}), str)

    def test_run_container_with_invalid_options(self):
        container = ContainerDocker("challenger_python")
        self.assertRaises(DockerException, container.run, {"--networkkkkk": "none"})

    def test_run_container_already_running(self):
        env = {"CONTAINER_TIME_OUT": 10}
        container = ContainerDocker("challenger_python", env=env)
        self.assertIsInstance(container.run(), str)
        self.assertRaises(DockerException, container.run)

    def test_kill_container_not_running(self):
        container = ContainerDocker("challenger_python")
        self.assertRaises(DockerException, container.kill)

    def test_kill_container_running(self):
        env = {"CONTAINER_TIME_OUT": 10}
        container = ContainerDocker("challenger_python", env=env)
        self.assertIsInstance(container.run(), str)
        self.assertTrue(container.kill())

    def test_container_is_running_with_container_not_running(self):
        container = ContainerDocker("challenger_python")
        self.assertFalse(container.is_running())

    def test_container_is_running_with_container_running(self):
        env = {"CONTAINER_TIME_OUT": 10}
        container = ContainerDocker("challenger_python", env=env)
        self.assertIsInstance(container.run(), str)
        self.assertTrue(container.is_running())

    def test_exec_command_with_container_not_running(self):
        container = ContainerDocker("challenger_python")
        self.assertRaises(DockerException, container.exec_command, ["echo", "test"])

    def test_exec_command_with_invalid_command(self):
        env = {"CONTAINER_TIME_OUT": 10}
        container = ContainerDocker("challenger_python", env=env)
        container.run()
        response = container.exec_command(["random command"])
        self.assertNotEqual(response.get("returncode"), 0)
        self.assertGreater(len(response.get("stdout")), 0)

    def test_exec_valid_command_in_container(self):
        env = {"CONTAINER_TIME_OUT": 10}
        container = ContainerDocker("challenger_python", env=env)
        container.run()
        response = container.exec_command(["echo", "test"])
        self.assertEqual(response.get("returncode"), 0)
        self.assertEqual(response.get("stdout"), "test")

    def test_copy_invalid_file_in_container(self):
        env = {"CONTAINER_TIME_OUT": 10}
        container = ContainerDocker("challenger_python", env=env)
        container.run()
        self.assertRaises(DockerException, container.copy_file, "random_file.py")

    def test_copy_file_in_container_not_running(self):
        container = ContainerDocker("challenger_python")
        self.assertRaises(DockerException, container.copy_file, "test.py")

    def test_copy_valid_file_in_container(self):
        env = {"CONTAINER_TIME_OUT": 10}
        container = ContainerDocker("challenger_python", env=env)
        container.run()
        self.assertTrue(container.copy_file("tests_container.py"))

