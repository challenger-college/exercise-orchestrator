import unittest

from docker.container import ContainerDocker

class TestDockerContainer(unittest.TestCase):

    def test_create_object(self):
        t = ContainerDocker("python")
        print(t)

