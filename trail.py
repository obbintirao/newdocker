import docker
from typing import Optional

client = docker.from_env()
xx=client.containers.get('e57c61c057e1').attrs

print(type(xx['Name']))
# res = client.login(username='osr2000', password='oO@096689', email='obbinti.rao@knowledgelens.com',
#                    registry='https://index.docker.io/v1')

# def testing_method(image: str, myDict: Optional[dict]):
#     if myDict:
#         s = client.containers.run(image,detach=True, **myDict)
#         print(s)
#     s = client.containers.run(image,detach=True)
#     print(s)
#
# testing_method('redis',{})


# def testing_method(image: str, myDict: Optional[dict]):
#     s = client.containers.run(image,detach=True, **myDict)
#     print(s)
# testing_method('redis',{})
# # testing_method('redis')




# print
# s = client.containers.run(image='redis', detach=True)
# print(s)c823b13533
# print(client.containers.get('c823b13533').status)

