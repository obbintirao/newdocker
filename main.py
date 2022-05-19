import fastapi
import pymongo.errors
from fastapi import FastAPI
from typing import Optional
from Exceptions import UniqueCredentialError
from test import myCollection,LaunchCredential, User, DockerExecutorEngine

app = FastAPI()


@app.post('/credentials', tags=["Enter Credentials"])
async def add_new_credentials(user: User):
    try:
        _id = myCollection.insert_one(dict(user))
        if _id:
            return {"status": "sucess"}

    # except pymongo.errors.DuplicateKeyError as d:
    #     print(d)
    #     return {"message": f"credential name already exist, try again! {d}"}
    except Exception as e:
        return {"status": "failed", "message": f"credential name already exist, try again! {e.__class__}"}, 500


@app.get("/credentials", tags=["List of Credentials"])
def employee_details(
        category: str = fastapi.Query(None, description="Enter Type of credentials or empty field will display all")):
    if category:
        return myCollection.find_one({"type": category}, {"_id": 0, "parameters": {"password": 0}})
    return list(myCollection.find({}, {"_id": 0, "parameters": {"password": 0}}))


"""class LaunchCredential(BaseModel): credential_name: Optional[str] = "satyam-creds" image: str variable_parameters: 
Optional[dict] = {"ports":{"8002":"5000"},"environment":{"key": "value"},"volumes":"(local_dir, "/webroot")"} 
"""


@app.post('/launchContainer', tags=["Enter details to launch container"])
def add_new_docker_credentials(user: LaunchCredential):
    docker_obj = DockerExecutorEngine(user.credential_name)
    try:
        return str(docker_obj.launch_container(user.image, **user.variable_parameters))
    except Exception:
        return {"status": "failed", "message": "Invalid input data, try again!"}, 500


# @app.post('/launchContainer', tags=["Enter details to launch container"])
# def add_new_docker_credentials(credentail_name: Optional[str] = None, image: str = None, data: Optional[dict] = {}):
#
#     docker_obj = DockerExecutorEngine(credentail_name)
#     return str(docker_obj.launch_container(image, **data))





@app.get("/status", tags=["Check the status of container"])
def status_of_launched_containers(Container_id: str = fastapi.Query(None, description="Enter conteiner ID or empty "
                                                                                      "field will display all "
                                                                                      "containers ")):
    docker_obj = DockerExecutorEngine()
    if Container_id:
        return docker_obj.container_status(Container_id)
    ll = (docker_obj.all_container_status())
    result = []
    for x in ll:
        result.append(x.id)
    return {"list_of_containers": result}





@app.get("/stop", tags=["Terminate container"])
def remove_containers(Container_id: str):
    docker_obj = DockerExecutorEngine()
    return docker_obj.terminate_container(Container_id)
