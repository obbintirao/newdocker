import docker
import pymongo
from typing import Optional
from pydantic import BaseModel

client = pymongo.MongoClient("mongodb://localhost:27017/")
# Access database
myDatabase = client['sankar_db']
# Access collection of the database
myCollection = myDatabase['docker_credentials']


class User(BaseModel):
    credential_name: str
    parameters: dict = {"Username": "osr2000", "password": "oO@096689", "email": "obbintisankarrao@gmail.com"}
    type: str = "docker/azure-blob"


class LaunchCredential(BaseModel):
    credential_name: Optional[str] = "satyam-creds"
    image: str
    variable_parameters: Optional[dict] = {"ports": {"8002": "5000"}, "environment": {"key": "value"}}


class DockerExecutorEngine:
    def __init__(self, credential_name=""):
        """
            credential-name:
            image-name(name:tag):
            env-variable:
            volume_mounts(optional):
            port-to-exposed:
            name-of-launched-container:
            tags(optional):
            network(optional):
            command(optional):
        """
        self.credential_name = credential_name
        self.client = docker.DockerClient.from_env()
        if self.credential_name:
            self.login_docker_account()

    def login_docker_account(self):
        ob = myCollection.find_one({"credential_name": self.credential_name, "type": "docker"},
                                   {"_id": 0, "credential_name": 0, "parameters": {"registry_name": 0}, "type": 0,
                                    "meta": 0})
        if not ob:
            raise ValueError("Invalid credentials")

        self.client.login(username=str(ob['parameters']['username']), password=str(ob['parameters']['password']),
                          email=str(ob['parameters']['email']),
                          registry='https://index.docker.io/v1')


    def launch_container(self, image, **kwargs):
        return self.client.containers.run(image=image, detach=True, **kwargs)



    def container_status(self, container_id):
        a = self.container_details(container_id)
        b = self.client.containers.get(container_id).status
        data = [container_id, a['Name']]
        resp = {"data": data, "status": b, "message": "Container launched successfully"}
        return resp

    def all_container_status(self):
        return self.client.containers.list()

    def container_details(self, container_id):
        return self.client.containers.get(container_id).attrs

    def stop_container(self, container_id):
        return self.client.containers.get(container_id).stop()

    def terminate_container(self, container_id):
        self.stop_container(container_id)
        return self.client.containers.get(container_id).remove()


if __name__ == "__main__":
    docker_obj = DockerExecutorEngine(credential_name="satyam-creds")
    res = docker_obj.login_docker_account()
    print(res)

    status = docker_obj.launch_container(image="redis:latest", detach=True, ports={800: 800})
    # status = docker_obj.launch_container(image="redis:latest", command=["/bin/sh", "-c", 'echo 1 && echo 2'],
    #                                      ports={10080: 8000},
    #                                      volumes={'/PycharmProjects/newdocker/': {'bind': '/mnt/vol2', 'mode': 'rw'},
    #                                               '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}})
    print(status)

    # print(docker_obj.stop_container("25d59d85223b"))
    # print(docker_obj.terminate_container('c823b13533'))
