# reference: https://www.youtube.com/watch?v=kCggyi_7pHg&t=804s
from fastapi import FastAPI
from pydantic import BaseModel
import requests

# the first thin is to create a model for our datastructure, that can be handleled by FastAPI converted
# to JSON. We use pydantic (typing)
class City(BaseModel):
    name: str
    timezone: str

# instantiate App object from fastApi
app = FastAPI()

# in memory database to hold things we want to display in WEB API
db=[]

#################################################
#Writing EndPoints
#################################################

#we can use decorators for endpoints to have access to http methods (get, post, put, delete)

@app.get(path="/")
def index():
    return {"key": "value"}

@app.get("/cities")
def get_cities(): #we simply go to in memory database and return all cities in db
    # WorldTimeAPI: let's get (request) the time zones for the cities we stored in in-memory databse, from an external web-server
    results = []
    for item in db:
        r = requests.get("http://worldtimeapi.org/api/timezone/{}".format(item["timezone"]))
        print(r.json())
        current_time = r.json()["datetime"] #convert the incoming results to json
        results.append({"name": item["name"], "timezone": item["timezone"], "currenttime": current_time})
    #return db # FastAPI automatically convert the data to JSON as long as is well-defined
    return results

@app.get("/cities/{city_id}")
def get_city(city_id: int):
    return db[city_id-1]


@app.post("/cities")
def create_city(city: City): # from this pydantic typing, FastAPI expect some data structure in the body of JSON request compatible with City class
    db.append(city.dict())
    # I want also to return the thing I just made in database
    return db[-1] # just the last item in in-memory database

@app.delete("/cities/{city_id}")
def delete_city(city_id: int):
    db.pop(city_id-1) # indexing in a list starts from 0, while in JSON request starts from 1
    return {} # return nothing